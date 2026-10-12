#!/usr/bin/env python3
"""Collect public ROS2 bug issues and linked PRs; Python standard library only."""
import argparse
import csv
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

REPOS = ['ros2/ros2', 'ros2/rclcpp', 'ros-navigation/navigation2',
         'ros-controls/ros2_control']
DEFAULT_OUT = Path(__file__).resolve().parents[1] / 'data' / 'ros2_faults'


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


class Client:
    def __init__(self, cache, delay):
        self.cache, self.delay = cache, delay
        self.cache.mkdir(parents=True, exist_ok=True)
        self.lock, self.last = threading.Lock(), 0.0
        self.patch_unavailable = False

    def get(self, url):
        # Persistent cache supports resuming without repeatedly hitting GitHub.
        key = hashlib.sha256(url.encode()).hexdigest()
        path = self.cache / (key + '.json.gz')
        if path.exists():
            return json.loads(gzip.decompress(path.read_bytes()))
        for attempt in range(3):
            with self.lock:
                time.sleep(max(0, self.delay - (time.monotonic() - self.last)))
                self.last = time.monotonic()
            try:
                request = urllib.request.Request(url, headers={
                    'User-Agent': 'ros2-fault-data-collector/1.0 (public research)',
                    'Accept': 'text/html, text/plain;q=0.9'})
                with urllib.request.urlopen(request, timeout=40) as response:
                    result = {'url': url, 'final_url': response.url,
                              'fetched_at': now(), 'http_status': response.status,
                              'text': response.read().decode('utf-8')}
                path.write_bytes(gzip.compress(json.dumps(result).encode()))
                return result
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504):
                    raise
                if attempt == 2:
                    raise
                time.sleep(min(30, int(exc.headers.get('Retry-After', 5 * (attempt + 1)))))
            except (urllib.error.URLError, TimeoutError) as exc:
                if 'Tunnel connection failed: 403' in str(exc):
                    raise
                if attempt == 2:
                    raise
                time.sleep(2 * (attempt + 1))


def payload(html, route):
    for script in re.findall(r'<script\b[^>]*type="application/json"[^>]*>(.*?)</script>', html, re.S):
        obj = json.loads(script)
        if route in obj.get('payload', {}):
            return obj['payload'][route]
    raise ValueError('GitHub page structure changed or login page: missing ' + route)


class PRParser(HTMLParser):
    """Extract rendered PR discussion bodies with block/code boundaries."""
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []
        self.bodies = []
        self.title_parts = []
        self.in_title = False
        self.links = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        if tag == 'a' and attrs.get('href'):
            self.links.add(attrs['href'])
        if self.depth:
            if tag not in self.VOID:
                self.depth += 1
            if tag in ('p', 'div', 'pre', 'br', 'li', 'h1', 'h2', 'h3', 'tr'):
                self.parts.append('\n')
            if tag == 'pre':
                self.parts.append('```\n')
        elif 'js-comment-body' in attrs.get('class', '').split():
            self.depth = 1
            self.parts = []

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if self.depth and tag not in self.VOID:
            if tag == 'pre':
                self.parts.append('\n```\n')
            if tag in ('p', 'div', 'li', 'h1', 'h2', 'h3'):
                self.parts.append('\n')
            self.depth -= 1
            if not self.depth:
                self.bodies.append(''.join(self.parts).strip())

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)
        if self.in_title:
            self.title_parts.append(data)


class DiffParser(HTMLParser):
    """Capture exposed code hunks, without claiming a complete/applicable patch."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.path = None
        self.files = {}
        self.depth = 0
        self.parts = []
        self.marker = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('data-path') and '{{' not in attrs['data-path']:
            self.path = attrs['data-path']
        if self.depth:
            if tag not in PRParser.VOID:
                self.depth += 1
        elif self.path and ('data-code-marker' in attrs or 'blob-code-hunk' in attrs.get('class', '').split()):
            self.depth = 1
            self.parts = []
            self.marker = attrs.get('data-code-marker')

    def handle_endtag(self, tag):
        if self.depth and tag not in PRParser.VOID:
            self.depth -= 1
            if not self.depth:
                text = ''.join(self.parts)
                if self.marker is not None or text.startswith('@@'):
                    self.files.setdefault(self.path, []).append((self.marker or '') + text)

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def provenance(response):
    return {k: response[k] for k in ('url', 'final_url', 'fetched_at', 'http_status')} | {
        'response_sha256': hashlib.sha256(response['text'].encode()).hexdigest()}


def collect_issue(client, repo, item, out):
    response = client.get(item['permalink'])
    issue = payload(response['text'], 'issueViewerRoute')['data']['repository']['issue']
    if issue['state'] != 'CLOSED' or not issue.get('body'):
        raise ValueError('Issue is no longer closed or has no body')
    # front and back timeline windows can overlap; deduplicate by event id.
    timeline = {}
    page_info = {}
    for key in ('timelineItems', 'backTimelineItems'):
        window = issue.get(key, {})
        page_info[key] = window.get('pageInfo', {})
        for edge in window.get('edges', []):
            node = edge['node']
            timeline[node['id']] = node
    events = sorted(timeline.values(), key=lambda x: (x.get('createdAt', ''), x['id']))
    comments = [e for e in events if e.get('__typename') == 'IssueComment']
    # Linked/closing PRs are confirmed relations; prose mentions stay separate.
    links = {}
    for key in ('linkedPullRequests', 'closedByPullRequestsReferences'):
        for pr in issue.get(key, {}).get('nodes', []):
            links.setdefault(pr['url'], {}).update(pr)
            links[pr['url']].setdefault('relation_types', []).append(key)
    for event in events:
        closer = event.get('closer') or {}
        if closer.get('__typename') == 'PullRequest':
            links.setdefault(closer['url'], {}).update(closer)
            links[closer['url']].setdefault('relation_types', []).append('closing_event')
    raw = {'schema_version': '1.0', 'repository': repo,
           'source': provenance(response),
           'issue': {k: issue.get(k) for k in (
               'id', 'databaseId', 'number', 'title', 'url', 'body', 'bodyHTML',
               'state', 'stateReason', 'createdAt', 'updatedAt', 'closedAt', 'author',
               'labels', 'totalCommentsCount', 'duplicateOf')},
           'comments': comments, 'timeline_events': events,
           'timeline_page_info': page_info, 'linked_pull_requests': list(links.values()),
           'comments_complete': len(comments) == issue.get('totalCommentsCount', -1),
           'linked_pr_fetches': []}
    for url, pr in links.items():
        entry = {'url': url, 'status': 'pending'}
        try:
            pr_response = client.get(url)
            parser = PRParser()
            parser.feed(pr_response['text'])
            if not parser.bodies:
                raise ValueError('PR body missing; page parser cannot validate extraction')
            match = re.fullmatch(r'https://github.com/([^/]+/[^/]+)/pull/(\d+)', url)
            if not match:
                raise ValueError('Unexpected PR URL')
            pr_repo, number = match.groups()
            pr_path = Path('raw/pull_requests') / pr_repo / (number + '.json')
            pr_raw = {'source': provenance(pr_response), 'url': url,
                      'title': ''.join(parser.title_parts),
                      'state_from_issue_link': pr.get('state'),
                      'body_rendered_text': parser.bodies[0],
                      'discussion_rendered_text': parser.bodies[1:],
                      'discussion_complete': None,
                      'commit_urls': sorted({urllib.parse.urljoin(url, link) for link in parser.links
                                             if re.search(r'/(?:commit|commits)/[0-9a-f]{40}$', link)}),
                      'note': 'Rendered page extraction; discussion completeness is not guaranteed.'}
            save(out / pr_path, pr_raw)
            entry.update(status='collected', raw_file=pr_path.as_posix())
            try:
                if client.patch_unavailable:
                    raise RuntimeError('Patch download destination blocked; using rendered changes')
                patch = client.get(url + '.patch')
                if not patch['text'].startswith('From ') or 'diff --git ' not in patch['text']:
                    raise ValueError('Response is not a Git patch')
                patch_path = pr_path.with_suffix('.patch')
                (out / patch_path).write_text(patch['text'], encoding='utf-8')
                entry.update(patch_file=patch_path.as_posix(), patch_source=provenance(patch))
            except Exception as exc:
                entry['patch_error'] = type(exc).__name__ + ': ' + str(exc)
                if 'Tunnel connection failed: 403' in str(exc):
                    client.patch_unavailable = True
                try:
                    changes = client.get(url + '/files')
                    diff_parser = DiffParser()
                    diff_parser.feed(changes['text'])
                    if not diff_parser.files:
                        raise ValueError('No exposed code hunks; diff may be collapsed or unavailable')
                    changes_path = pr_path.with_suffix('.changes.json')
                    save(out / changes_path, {
                        'source': provenance(changes), 'files': diff_parser.files,
                        'complete': None, 'format': 'rendered_diff_lines',
                        'note': 'Exposed code hunks only; not a complete patch or verified fix.'})
                    entry['rendered_changes_file'] = changes_path.as_posix()
                except Exception as diff_exc:
                    entry['rendered_changes_error'] = type(diff_exc).__name__ + ': ' + str(diff_exc)
        except Exception as exc:
            entry.update(status='failed', error=type(exc).__name__ + ': ' + str(exc))
        raw['linked_pr_fetches'].append(entry)
    path = Path('raw/issues') / repo / (str(issue['number']) + '.json')
    save(out / path, raw)
    return raw, path.as_posix()


def normalize(raw, path):
    issue = raw['issue']
    texts = [(issue['url'], issue['body'])] + [
        (c.get('url') or issue['url'] + '#issuecomment-' + str(c.get('databaseId', '')),
         c.get('body', '')) for c in raw['comments']]
    blocks, error_lines, candidates = [], [], []
    for url, text in texts:
        for match in re.finditer(r'```([^\n`]*)\n(.*?)```', text, re.S):
            blocks.append({'source_url': url, 'language': match[1].strip(), 'text': match[2].strip()})
        for line in text.splitlines():
            if re.search(r'\b(error|exception|traceback|segmentation fault|fatal|assertion failed)\b', line, re.I):
                error_lines.append({'source_url': url, 'text': line})
        if url != issue['url'] and re.search(r'\b(fixed|fixes|resolved|workaround|solved|works now|root cause)\b', text, re.I):
            candidates.append({'source_url': url, 'text': text, 'verified': False})
    combined = '\n'.join(t for _, t in texts).lower()
    categories = []
    for name, pattern in {
        'build_install': r'colcon|cmake|compil|linker|undefined reference|install',
        'communication_qos': r'\bqos\b|\bdds\b|\brmw\b|publisher|subscription|discovery',
        'executor_concurrency': r'executor|deadlock|race condition|data race|callback|thread',
        'navigation': r'costmap|planner|controller server|navigation|\bnav2\b|localization',
        'tf_time': r'\btf2?\b|transform|clock|timestamp|sim.time',
        'control_hardware': r'ros2_control|hardware.interface|controller.manager|joint|actuator',
        'simulation': r'gazebo|ignition|simulation',
        'runtime_crash': r'segmentation|segfault|crash|exception|abort',
        'parameters_lifecycle': r'parameter|lifecycle|configure|activate',
    }.items():
        if re.search(pattern, combined):
            categories.append(name)
    distros = sorted(set(re.findall(r'\b(foxy|galactic|humble|iron|jazzy|kilted|lyrical|rolling)\b', combined)))
    return {'case_id': raw['repository'].replace('/', '__') + '__' + str(issue['number']),
            'repository': raw['repository'], 'issue_number': issue['number'],
            'source_url': issue['url'], 'title': issue['title'],
            'created_at': issue['createdAt'], 'updated_at': issue['updatedAt'],
            'closed_at': issue.get('closedAt') or next((e['createdAt'] for e in reversed(raw['timeline_events']) if e['__typename'] == 'ClosedEvent'), None),
            'state': issue['state'], 'state_reason': issue['stateReason'],
            'labels': [e['node']['name'] for e in (issue.get('labels') or {}).get('edges', [])],
            'category_hints': categories or ['other'], 'ros_distro_mentions': distros,
            'fault_phenomenon': {'title': issue['title'], 'description': issue['body']},
            'error_logs': error_lines, 'code_and_log_blocks': blocks,
            'fault_cause': None, 'troubleshooting_steps': None,
            'solution': None, 'verification_result': None,
            'solution_evidence_candidates': candidates,
            'comments': [{'source_url': url, 'body': text} for url, text in texts[1:]],
            'comment_count_expected': issue.get('totalCommentsCount'),
            'comment_count_collected': len(raw['comments']),
            'comments_complete': raw['comments_complete'],
            'linked_pull_requests': raw['linked_pull_requests'],
            'linked_pr_fetches': raw['linked_pr_fetches'],
            'raw_file': path, 'fetched_at': raw['source']['fetched_at'],
            'content_sha256': hashlib.sha256(issue['body'].encode()).hexdigest(),
            'review_status': 'unreviewed', 'training_ready': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repos', nargs='+', default=REPOS)
    parser.add_argument('--per-repo', type=int, default=25)
    parser.add_argument('--max-pages', type=int, default=5)
    parser.add_argument('--workers', type=int, default=2)
    parser.add_argument('--delay', type=float, default=0.5)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--cache', type=Path, default=Path('/tmp/ros2-fault-collector-cache'))
    args = parser.parse_args()
    if args.per_repo < 1 or args.max_pages < 1 or args.workers < 1 or args.delay < 0:
        parser.error('counts must be positive and delay nonnegative')
    for repo in args.repos:
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', repo):
            parser.error('invalid repository: ' + repo)
    args.output.mkdir(parents=True, exist_ok=True)
    client = Client(args.cache, args.delay)
    run = {'started_at': now(), 'transport': 'github_public_html',
           'query': 'is:issue is:closed label:bug sort:updated-desc',
           'target_per_repository': args.per_repo, 'repositories': args.repos,
           'selection': [], 'failures': []}
    cases, seen = [], set()
    for repo in args.repos:
        items = []
        try:
            for page in range(1, args.max_pages + 1):
                query = urllib.parse.urlencode({'q': run['query'], 'page': page})
                response = client.get('https://github.com/' + repo + '/issues?' + query)
                result = payload(response['text'], 'issuesIndexContentRoute')
                run['selection'].append({'repository': repo, 'page': page,
                                         'source': provenance(response), 'page_info': result['pageInfo']})
                items.extend(x['issue'] for x in result['results'] if 'issue' in x)
                if len(items) >= args.per_repo or page >= result['pageInfo']['totalPages']:
                    break
        except Exception as exc:
            run['failures'].append({'repository': repo, 'stage': 'list', 'error': str(exc)})
        items = items[:args.per_repo]
        print(repo + ': selected ' + str(len(items)), flush=True)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [(item, pool.submit(collect_issue, client, repo, item, args.output)) for item in items]
            for item, future in futures:
                try:
                    raw, path = future.result()
                    case = normalize(raw, path)
                    if case['source_url'] not in seen:
                        cases.append(case)
                        seen.add(case['source_url'])
                    print('  collected #' + str(item['number']), flush=True)
                except Exception as exc:
                    run['failures'].append({'repository': repo, 'issue_number': item['number'],
                                            'stage': 'issue', 'error': type(exc).__name__ + ': ' + str(exc)})
                    print('  FAILED #' + str(item['number']) + ': ' + str(exc), flush=True)
    cases.sort(key=lambda x: (x['repository'], x['issue_number']))
    with (args.output / 'cases.jsonl').open('w', encoding='utf-8') as f:
        for case in cases:
            f.write(json.dumps(case, ensure_ascii=False) + '\n')
    with (args.output / 'catalog.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['case_id', 'repository', 'issue_number', 'title', 'source_url',
                         'category_hints', 'ros_distro_mentions', 'comments_collected',
                         'comments_expected', 'comments_complete', 'linked_pr_count', 'raw_file'])
        for c in cases:
            writer.writerow([c['case_id'], c['repository'], c['issue_number'], c['title'],
                             c['source_url'], ';'.join(c['category_hints']),
                             ';'.join(c['ros_distro_mentions']), c['comment_count_collected'],
                             c['comment_count_expected'], c['comments_complete'],
                             len(c['linked_pull_requests']), c['raw_file']])
    run.update(finished_at=now(), collected_cases=len(cases),
               counts_by_repository=dict(Counter(c['repository'] for c in cases)),
               category_hint_counts=dict(Counter(label for c in cases for label in c['category_hints'])),
               comments_collected=sum(c['comment_count_collected'] for c in cases),
               cases_with_incomplete_comments=sum(not c['comments_complete'] for c in cases),
               code_and_log_blocks=sum(len(c['code_and_log_blocks']) for c in cases),
               linked_pr_urls=len({p['url'] for c in cases for p in c['linked_pull_requests']}),
               pr_records_collected=len({p['url'] for c in cases for p in c['linked_pr_fetches'] if p['status'] == 'collected'}),
               patches_collected=len({p['url'] for c in cases for p in c['linked_pr_fetches'] if 'patch_file' in p}),
               rendered_changes_collected=len({p['url'] for c in cases for p in c['linked_pr_fetches'] if 'rendered_changes_file' in p}),
               pr_fetch_failures=[p for c in cases for p in c['linked_pr_fetches'] if p['status'] != 'collected'],
               patch_fetch_failures=[p for c in cases for p in c['linked_pr_fetches'] if 'patch_error' in p])
    save(args.output / 'collection_report.json', run)
    index = ['# ROS2 故障案例索引', '',
             '原始采集数据；类别由关键词粗分，关闭不代表已验证修复。', '',
             '| 项目 | Issue | 标题 | 评论（采集/总数） | 关联 PR |',
             '| --- | --- | --- | --- | --- |']
    for c in cases:
        title = c['title'].replace('|', '\\|').replace('\n', ' ')
        prs = ', '.join('[#' + str(p['number']) + '](' + p['url'] + ')' for p in c['linked_pull_requests']) or '—'
        index.append(f"| {c['repository']} | [#{c['issue_number']}]({c['source_url']}) | {title} | {c['comment_count_collected']}/{c['comment_count_expected']} | {prs} |")
    (args.output / 'INDEX.md').write_text('\n'.join(index) + '\n', encoding='utf-8')
    print(json.dumps({k: run[k] for k in ('collected_cases', 'counts_by_repository', 'comments_collected', 'cases_with_incomplete_comments', 'linked_pr_urls')}, ensure_ascii=False), flush=True)
    # Do not report success if selected issue fetches failed or a repo is short.
    return 1 if run['failures'] or any(run['counts_by_repository'].get(r, 0) < args.per_repo for r in args.repos) else 0


if __name__ == '__main__':
    raise SystemExit(main())

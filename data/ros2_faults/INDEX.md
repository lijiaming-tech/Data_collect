# ROS2 故障案例索引

原始采集数据；类别由关键词粗分，关闭不代表已验证修复。

| 项目 | Issue | 标题 | 评论（采集/总数） | 关联 PR |
| --- | --- | --- | --- | --- |
| ros-controls/ros2_control | [#1095](https://github.com/ros-controls/ros2_control/issues/1095) | view_controller_chains does not work with example | 6/6 | [#2026](https://github.com/ros-controls/ros2_control/pull/2026) |
| ros-controls/ros2_control | [#2415](https://github.com/ros-controls/ros2_control/issues/2415) | rqt_controller_manager stuck | 11/11 | — |
| ros-controls/ros2_control | [#2496](https://github.com/ros-controls/ros2_control/issues/2496) | Coverage report is missing some files | 1/1 | [#3522](https://github.com/ros-controls/ros2_control/pull/3522) |
| ros-controls/ros2_control | [#2508](https://github.com/ros-controls/ros2_control/issues/2508) | Deactivate controllers when hardware component is inactive | 5/5 | — |
| ros-controls/ros2_control | [#2680](https://github.com/ros-controls/ros2_control/issues/2680) | AsynFunctionHandler: pure virtual method called | 7/7 | [#3321](https://github.com/ros-controls/ros2_control/pull/3321) |
| ros-controls/ros2_control | [#2968](https://github.com/ros-controls/ros2_control/issues/2968) | unable to require state interfaces exported by chainable controller | 8/8 | — |
| ros-controls/ros2_control | [#2975](https://github.com/ros-controls/ros2_control/issues/2975) | CM is calling update of a controller after cleanup | 4/4 | — |
| ros-controls/ros2_control | [#3084](https://github.com/ros-controls/ros2_control/issues/3084) | Data race in ControllerManager::update() (controller_manager.cpp:2186) | 9/9 | — |
| ros-controls/ros2_control | [#3102](https://github.com/ros-controls/ros2_control/issues/3102) | multi_ctrls_test_type_in_param fails with runtime_error | 4/4 | [#3109](https://github.com/ros-controls/ros2_control/pull/3109) |
| ros-controls/ros2_control | [#3123](https://github.com/ros-controls/ros2_control/issues/3123) | Segfault in in `joint_state_broadcaster::JointStateBroadcaster::init_joint_data()` | 5/5 | — |
| ros-controls/ros2_control | [#3153](https://github.com/ros-controls/ros2_control/issues/3153) | configure_controller error path causes controller manager to hang for invalid chainable controllers | 2/2 | [#3192](https://github.com/ros-controls/ros2_control/pull/3192) |
| ros-controls/ros2_control | [#3211](https://github.com/ros-controls/ros2_control/issues/3211) | reference interfaces recursively prepended with controller name after reconfiguration | 2/2 | [#3212](https://github.com/ros-controls/ros2_control/pull/3212) |
| ros-controls/ros2_control | [#3220](https://github.com/ros-controls/ros2_control/issues/3220) | Zero controller update rate might trigger undefined behavior | 2/2 | [#3454](https://github.com/ros-controls/ros2_control/pull/3454) |
| ros-controls/ros2_control | [#3233](https://github.com/ros-controls/ros2_control/issues/3233) | `from_chars` is not a member of `std` | 0/0 | [#3234](https://github.com/ros-controls/ros2_control/pull/3234) |
| ros-controls/ros2_control | [#3240](https://github.com/ros-controls/ros2_control/issues/3240) | lexical_casts: Behavior change with charconv | 1/1 | [#3244](https://github.com/ros-controls/ros2_control/pull/3244) |
| ros-controls/ros2_control | [#3269](https://github.com/ros-controls/ros2_control/issues/3269) | `std::clamp` assertion on Resolute Racoon | 1/1 | [#3275](https://github.com/ros-controls/ros2_control/pull/3275) |
| ros-controls/ros2_control | [#3279](https://github.com/ros-controls/ros2_control/issues/3279) | Issue with `constexpr std::array` on Resolute Racoon | 1/1 | [#3282](https://github.com/ros-controls/ros2_control/pull/3282) |
| ros-controls/ros2_control | [#3283](https://github.com/ros-controls/ros2_control/issues/3283) | Issue with `constexpr std::vector` on Resolute Racoon | 0/0 | [#3287](https://github.com/ros-controls/ros2_control/pull/3287) |
| ros-controls/ros2_control | [#3308](https://github.com/ros-controls/ros2_control/issues/3308) | Unset fallback_controllers list warnings | 0/0 | [#3270](https://github.com/ros-controls/ros2_control/pull/3270) |
| ros-controls/ros2_control | [#3364](https://github.com/ros-controls/ros2_control/issues/3364) | rqt_controller_manager crash on lyrical | 2/2 | [#3367](https://github.com/ros-controls/ros2_control/pull/3367), [#3366](https://github.com/ros-controls/ros2_control/pull/3366) |
| ros-controls/ros2_control | [#3416](https://github.com/ros-controls/ros2_control/issues/3416) | Spawning controllers with type declaration | 1/1 | — |
| ros-controls/ros2_control | [#3495](https://github.com/ros-controls/ros2_control/issues/3495) | `ros2_control_node` fails to start up on Windows/RoboStack in Jazzy or newer | 8/8 | — |
| ros-controls/ros2_control | [#3591](https://github.com/ros-controls/ros2_control/issues/3591) | rqt_controller_manager still fails on SIGINT | 1/1 | — |
| ros-controls/ros2_control | [#3593](https://github.com/ros-controls/ros2_control/issues/3593) | GenericSystem rejects controller reference interfaces when calculate_dynamics is enabled | 0/0 | [#3596](https://github.com/ros-controls/ros2_control/pull/3596) |
| ros-controls/ros2_control | [#3612](https://github.com/ros-controls/ros2_control/issues/3612) | Data race on overruns.print_warnings during diagnostic parameter refresh | 0/0 | [#3619](https://github.com/ros-controls/ros2_control/pull/3619), [#1](https://github.com/Quchaosheng/ros2_control/pull/1) |
| ros-navigation/navigation2 | [#1999](https://github.com/ros-navigation/navigation2/issues/1999) | Nav2 plans path through walls when there is no other way to reach the goal | 18/18 | — |
| ros-navigation/navigation2 | [#3767](https://github.com/ros-navigation/navigation2/issues/3767) | MPPI crashing on loading plug-ings  | 28/48 | — |
| ros-navigation/navigation2 | [#4722](https://github.com/ros-navigation/navigation2/issues/4722) | Online example is not working on ros2 jazzy  | 18/18 | — |
| ros-navigation/navigation2 | [#4754](https://github.com/ros-navigation/navigation2/issues/4754) | [nav2_rviz_plugins/Selector] Unable to set goal pose if we run rviz2 later | 14/14 | [#4882](https://github.com/ros-navigation/navigation2/pull/4882) |
| ros-navigation/navigation2 | [#4884](https://github.com/ros-navigation/navigation2/issues/4884) | Fix flaky dwb_critics test ObstacleFootprint.LineCost - maybe related to AddressSanitizer: heap-buffer-overflow READ | 1/1 | — |
| ros-navigation/navigation2 | [#5088](https://github.com/ros-navigation/navigation2/issues/5088) | MPPI GoalCritic and Path Inversion Bug | 10/10 | [#5105](https://github.com/ros-navigation/navigation2/pull/5105) |
| ros-navigation/navigation2 | [#5100](https://github.com/ros-navigation/navigation2/issues/5100) | Bug in parameter configuration in controller. | 2/2 | [#5106](https://github.com/ros-navigation/navigation2/pull/5106) |
| ros-navigation/navigation2 | [#5144](https://github.com/ros-navigation/navigation2/issues/5144) | DockRobot fails without reason if the robot is already docked in the requested charging dock | 2/2 | [#5171](https://github.com/ros-navigation/navigation2/pull/5171) |
| ros-navigation/navigation2 | [#5192](https://github.com/ros-navigation/navigation2/issues/5192) | nav2_smac_planner,  path is not continuous | 14/20 | [#5207](https://github.com/ros-navigation/navigation2/pull/5207) |
| ros-navigation/navigation2 | [#5232](https://github.com/ros-navigation/navigation2/issues/5232) | Local and global costmap ~half cell misalignment when both using the global frame | 9/9 | [#6039](https://github.com/ros-navigation/navigation2/pull/6039) |
| ros-navigation/navigation2 | [#5324](https://github.com/ros-navigation/navigation2/issues/5324) | Would a planner recovery help - ComputePathThroughPoses | 6/6 | [#5326](https://github.com/ros-navigation/navigation2/pull/5326) |
| ros-navigation/navigation2 | [#5330](https://github.com/ros-navigation/navigation2/issues/5330) | SMAC smoother can generate infeasible paths when using non-circular robots in very confined spaces | 11/11 | [#6257](https://github.com/ros-navigation/navigation2/pull/6257), [#5462](https://github.com/ros-navigation/navigation2/pull/5462), [#6202](https://github.com/ros-navigation/navigation2/pull/6202) |
| ros-navigation/navigation2 | [#5464](https://github.com/ros-navigation/navigation2/issues/5464) | MPPI acceleration constraints not respected | 12/12 | [#5467](https://github.com/ros-navigation/navigation2/pull/5467) |
| ros-navigation/navigation2 | [#5465](https://github.com/ros-navigation/navigation2/issues/5465) | MPPI asymmetric accelerations cause slower trajectories  | 6/6 | [#6072](https://github.com/ros-navigation/navigation2/pull/6072) |
| ros-navigation/navigation2 | [#5472](https://github.com/ros-navigation/navigation2/issues/5472) | SMAC smooth_path dynamic parameter causes crash | 4/4 | [#5473](https://github.com/ros-navigation/navigation2/pull/5473) |
| ros-navigation/navigation2 | [#5503](https://github.com/ros-navigation/navigation2/issues/5503) | MPPI navigation regression from 1.1.17 to 1.1.18 on Humble | 5/5 | [#5527](https://github.com/ros-navigation/navigation2/pull/5527) |
| ros-navigation/navigation2 | [#5595](https://github.com/ros-navigation/navigation2/issues/5595) | [RPP] min_distance_to_obstacle and velocity_scaled_lookahead dont work well together when min_lookahead < min_distance_to_obstacle | 5/5 | [#5598](https://github.com/ros-navigation/navigation2/pull/5598), [#5616](https://github.com/ros-navigation/navigation2/pull/5616) |
| ros-navigation/navigation2 | [#5626](https://github.com/ros-navigation/navigation2/issues/5626) | backward motion at begining of the path(maybe a bug)  generated by nav2_smac_planner (hybrid a star) | 11/11 | [#5802](https://github.com/ros-navigation/navigation2/pull/5802), [#5653](https://github.com/ros-navigation/navigation2/pull/5653), [#5669](https://github.com/ros-navigation/navigation2/pull/5669), [#5670](https://github.com/ros-navigation/navigation2/pull/5670) |
| ros-navigation/navigation2 | [#5671](https://github.com/ros-navigation/navigation2/issues/5671) | SMAC Hybrid Visualization Offset from Expansions to Path | 5/5 | [#6040](https://github.com/ros-navigation/navigation2/pull/6040) |
| ros-navigation/navigation2 | [#5943](https://github.com/ros-navigation/navigation2/issues/5943) | nav2_costmap_2d reports test success despite internal failures | 14/14 | [#5974](https://github.com/ros-navigation/navigation2/pull/5974) |
| ros-navigation/navigation2 | [#6030](https://github.com/ros-navigation/navigation2/issues/6030) | bad_weak_ptr and Race Condition on ARM64 | 9/9 | — |
| ros-navigation/navigation2 | [#6045](https://github.com/ros-navigation/navigation2/issues/6045) | question about SimpleChargingDock external detection rotation | 2/2 | — |
| ros-navigation/navigation2 | [#6226](https://github.com/ros-navigation/navigation2/issues/6226) | [nav2_behavior_tree] TruncatePathLocal action uses robot base frame id only from input port and not from parameter file | 4/4 | [#6242](https://github.com/ros-navigation/navigation2/pull/6242) |
| ros-navigation/navigation2 | [#6267](https://github.com/ros-navigation/navigation2/issues/6267) | [nav2_costmap_2d] Jazzy: costmap_2d_publisher does not publish costmap when no subscribers are present at launching time | 2/2 | [#6324](https://github.com/ros-navigation/navigation2/pull/6324), [#6272](https://github.com/ros-navigation/navigation2/pull/6272) |
| ros-navigation/navigation2 | [#6398](https://github.com/ros-navigation/navigation2/issues/6398) | Theta* generatePath skips expanding the last popped node (false no-path) | 2/2 | [#6401](https://github.com/ros-navigation/navigation2/pull/6401) |
| ros2/rclcpp | [#1698](https://github.com/ros2/rclcpp/issues/1698) | rclcpp_components_register_nodes() fails if not in the project's root CMakeLists.txt | 4/4 | [#3064](https://github.com/ros2/rclcpp/pull/3064) |
| ros2/rclcpp | [#2220](https://github.com/ros2/rclcpp/issues/2220) | AddressSanitizer: new-delete-type-mismatch | 21/21 | — |
| ros2/rclcpp | [#2462](https://github.com/ros2/rclcpp/issues/2462) | max_duration not respected in spin_some for StaticSingleThreadedExecutor and EventsExecutor | 4/4 | [#2465](https://github.com/ros2/rclcpp/pull/2465), [#3121](https://github.com/ros2/rclcpp/pull/3121) |
| ros2/rclcpp | [#2898](https://github.com/ros2/rclcpp/issues/2898) | Faulty boundary condition check in dynamic parameter update of floating point parameters | 3/3 | [#3143](https://github.com/ros2/rclcpp/pull/3143) |
| ros2/rclcpp | [#2911](https://github.com/ros2/rclcpp/issues/2911) | use_intra_process_comms bypasses topic statistics computation | 1/1 | [#3130](https://github.com/ros2/rclcpp/pull/3130), [#2913](https://github.com/ros2/rclcpp/pull/2913) |
| ros2/rclcpp | [#2926](https://github.com/ros2/rclcpp/issues/2926) | 🧑‍🌾 Flaky test `TestExecutor.spin_all_fail_wait_set_clear` in Linux | 8/8 | — |
| ros2/rclcpp | [#2947](https://github.com/ros2/rclcpp/issues/2947) | MSVC build problems | 6/6 | [#3043](https://github.com/ros2/rclcpp/pull/3043) |
| ros2/rclcpp | [#2948](https://github.com/ros2/rclcpp/issues/2948) | ServerGoalHandle may throw from a destructor | 6/6 | [#2953](https://github.com/ros2/rclcpp/pull/2953) |
| ros2/rclcpp | [#2980](https://github.com/ros2/rclcpp/issues/2980) | 🧑‍🌾  `test_allocator_memory_strategy` failing in Rolling Connext CI | 8/8 | — |
| ros2/rclcpp | [#2983](https://github.com/ros2/rclcpp/issues/2983) | :farmer: `gtest.missing_result` test failing because freezes in `GenericClient.take_response` in Kilted | 2/2 | — |
| ros2/rclcpp | [#3001](https://github.com/ros2/rclcpp/issues/3001) | Tf related topics do not get properly namespaced in Composable Nodes | 6/6 | — |
| ros2/rclcpp | [#3020](https://github.com/ros2/rclcpp/issues/3020) | `wait_for_message` uses default ros context instead of passed node's context | 0/0 | [#3021](https://github.com/ros2/rclcpp/pull/3021) |
| ros2/rclcpp | [#3035](https://github.com/ros2/rclcpp/issues/3035) | AddressSanitizer reports new-delete-type-mismatch when creating rclcpp::Node via make_shared | 1/1 | — |
| ros2/rclcpp | [#3036](https://github.com/ros2/rclcpp/issues/3036) | subscriber node uses 100% cpu when publisher disconnects (recent regression) | 10/10 | — |
| ros2/rclcpp | [#3065](https://github.com/ros2/rclcpp/issues/3065) | rclcpp.TestNode.ConfigureNodesFilterAndCheckAddParameterEventCallback failure | 6/6 | [#3085](https://github.com/ros2/rclcpp/pull/3085) |
| ros2/rclcpp | [#3117](https://github.com/ros2/rclcpp/issues/3117) | `ServerGoalHandle::publish_feedback()` does not enforce precondition that goal must be in EXECUTING state | 0/0 | [#3118](https://github.com/ros2/rclcpp/pull/3118) |
| ros2/rclcpp | [#3128](https://github.com/ros2/rclcpp/issues/3128) | :farmer: Warning in Jazzy ci connext regarding uninitialized variables in GenericClient (status_offset, result_offset) | 1/1 | — |
| ros2/rclcpp | [#3154](https://github.com/ros2/rclcpp/issues/3154) | :farmer: rclcpp TestBusyWaiting failing in nightly linux repeated/rhel debug by a clock difference | 3/3 | — |
| ros2/rclcpp | [#3172](https://github.com/ros2/rclcpp/issues/3172) | Race condition in executor when canceling before spin | 1/1 | [#3174](https://github.com/ros2/rclcpp/pull/3174) |
| ros2/rclcpp | [#3175](https://github.com/ros2/rclcpp/issues/3175) | EventsCBGExecutor treats reentrant callback groups like they're mutually exclusive | 10/10 | [#3178](https://github.com/ros2/rclcpp/pull/3178) |
| ros2/rclcpp | [#3182](https://github.com/ros2/rclcpp/issues/3182) | Data race on the random number generator used in rclcpp_action for creating the UUID | 0/0 | [#3183](https://github.com/ros2/rclcpp/pull/3183) |
| ros2/rclcpp | [#3191](https://github.com/ros2/rclcpp/issues/3191) | `RCLCPP_PUBLIC [[deprecated]]` fails to build on debian12+gcc12 | 3/3 | — |
| ros2/rclcpp | [#3222](https://github.com/ros2/rclcpp/issues/3222) | Race condition when loading multiple isolated component_container | 0/0 | [#3223](https://github.com/ros2/rclcpp/pull/3223) |
| ros2/rclcpp | [#3232](https://github.com/ros2/rclcpp/issues/3232) | TSan lock-order-inversion reproducible via Nav2 test_bond | 3/3 | [#3241](https://github.com/ros2/rclcpp/pull/3241) |
| ros2/rclcpp | [#3257](https://github.com/ros2/rclcpp/issues/3257) | Malformed SetParameters request with invalid type crashes rclcpp node | 3/3 | [#3256](https://github.com/ros2/rclcpp/pull/3256) |
| ros2/ros2 | [#1613](https://github.com/ros2/ros2/issues/1613) | DSV files are not sourced in binary workspace | 13/13 | — |
| ros2/ros2 | [#1670](https://github.com/ros2/ros2/issues/1670) | ROS2 packages failing to build from source with new cmake version 4.0.0 | 3/3 | — |
| ros2/ros2 | [#1696](https://github.com/ros2/ros2/issues/1696) | Can't install docker. Key is expired | 6/6 | — |
| ros2/ros2 | [#1705](https://github.com/ros2/ros2/issues/1705) | latest source build failed with urdfdom | 3/3 | [#222](https://github.com/ros/urdfdom/pull/222) |
| ros2/ros2 | [#1706](https://github.com/ros2/ros2/issues/1706) | source build ubuntu setup seems broken. | 15/15 | — |
| ros2/ros2 | [#1710](https://github.com/ros2/ros2/issues/1710) | "failed to create process." when running ros2 commads. | 2/2 | — |
| ros2/ros2 | [#1717](https://github.com/ros2/ros2/issues/1717) | rqt_graph command in tutorial requires full ros2 run invocation | 0/0 | [#5821](https://github.com/ros2/ros2_documentation/pull/5821) |
| ros2/ros2 | [#1722](https://github.com/ros2/ros2/issues/1722) | [Jazzy][Python] QoS compatibility issue when setting the liveliness of pub/sub to `BEST_AVAILABLE` | 6/6 | [#84](https://github.com/ros2/rmw_dds_common/pull/84), [#1561](https://github.com/ros2/rclpy/pull/1561) |
| ros2/ros2 | [#1754](https://github.com/ros2/ros2/issues/1754) | All Python Generated Messages Broken (testing repo) | 7/7 | — |
| ros2/ros2 | [#1756](https://github.com/ros2/ros2/issues/1756) | Ros2 Humble deb installation on Ubuntu 22.04.5 LTS - Incompatible packages | 2/2 | — |
| ros2/ros2 | [#1758](https://github.com/ros2/ros2/issues/1758) | Windows, Pixi, VS2022 v17.14: Increase opencv version from 4.9.0 to 4.10.0 | 2/2 | — |
| ros2/ros2 | [#1759](https://github.com/ros2/ros2/issues/1759) | ROS2 Abnormal CPU usage in many node. | 4/4 | — |
| ros2/ros2 | [#1770](https://github.com/ros2/ros2/issues/1770) | Core ROS 2 package has `ros-kilted-rmw-zenoh-cpp` as direct dependency | 2/2 | [#60](https://github.com/ros2/ament_cmake_ros/pull/60) |
| ros2/ros2 | [#1775](https://github.com/ros2/ros2/issues/1775) | Unable to install ros-humble-librealsense2 DEB package on systems with automounted homes | 3/3 | — |
| ros2/ros2 | [#1777](https://github.com/ros2/ros2/issues/1777) | [rcl_yaml_param_parser] Heap-buffer-overflow in namespace handling (add_name_to_ns / rem_name_from_ns) | 8/8 | [#1281](https://github.com/ros2/rcl/pull/1281) |
| ros2/ros2 | [#1779](https://github.com/ros2/ros2/issues/1779) | The releases have incorrect files ARM has x86 files and AMD has aarch64 files in packages | 3/3 | — |
| ros2/ros2 | [#1789](https://github.com/ros2/ros2/issues/1789) | [Jazzy] Broken libzstd dependency on Ubuntu 24.04 (arm64/Raspberry Pi) prevents apt installation | 9/9 | [#6213](https://github.com/ros2/ros2_documentation/pull/6213) |
| ros2/ros2 | [#1797](https://github.com/ros2/ros2/issues/1797) | Cannot install Kilted on 24.04.3 server (works on desktop) | 5/5 | — |
| ros2/ros2 | [#1807](https://github.com/ros2/ros2/issues/1807) | :farmer: project root test_wait failing by an uninplemented `rmw_subscription_get_content_filter` | 1/1 | — |
| ros2/ros2 | [#1809](https://github.com/ros2/ros2/issues/1809) | Foxglove bridge missing from repositories | 2/2 | — |
| ros2/ros2 | [#1819](https://github.com/ros2/ros2/issues/1819) | Dependency issues during installation on Ubuntu 22.04.5 LTS | 2/3 | — |
| ros2/ros2 | [#1838](https://github.com/ros2/ros2/issues/1838) | [Lyrical T&T] 404 Not Found during Debian Install on Ubuntu 26.04 (AMD64) | 3/4 | — |
| ros2/ros2 | [#1851](https://github.com/ros2/ros2/issues/1851) | [Lyrical]: bounded dynamic boolean arrays fail to compile with Fast CDR C++ typesupport | 2/2 | — |
| ros2/ros2 | [#1864](https://github.com/ros2/ros2/issues/1864) | Add clang-tidy to the Pixi environment | 0/0 | [#1865](https://github.com/ros2/ros2/pull/1865) |
| ros2/ros2 | [#1877](https://github.com/ros2/ros2/issues/1877) | Documentation for ROS2 Lyrical packages missing from https://docs.ros.org/en/lyrical/p/ | 6/6 | — |

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'fastbot_slam'
    pkg_dir = get_package_share_directory(pkg_name)
    nav2_yaml = os.path.join(pkg_dir, 'config', 'amcl_sim.yaml')
    map_file = os.path.join(pkg_dir, 'config', 'cp21_map_sim.yaml')
    rviz_file = os.path.join(pkg_dir, 'rviz', 'navigation.rviz')
    controller_yaml = os.path.join(pkg_dir, 'config', 'controller.yaml')
    bt_navigator_yaml = os.path.join(pkg_dir, 'config', 'bt_navigator.yaml')
    planner_yaml = os.path.join(pkg_dir, 'config', 'planner_server.yaml')
    recovery_yaml = os.path.join(pkg_dir, 'config', 'recovery.yaml')
    filters_yaml = os.path.join(pkg_dir, 'config', 'filters.yaml')

    
    return LaunchDescription([     
         Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[{'use_sim_time': True}, 
                        {'yaml_filename':map_file}]
        ),

        Node(
            package='nav2_map_server',
            executable='map_server',
            name='filter_mask_server',
            output='screen',
            emulate_tty=True,
            parameters=[filters_yaml]
        ),


        Node(
            package='nav2_map_server',
            executable='costmap_filter_info_server',
            name='costmap_filter_info_server',
            output='screen',
            emulate_tty=True,
            parameters=[filters_yaml]
        ),
            
        Node(
            package='nav2_amcl',
            executable='amcl',
            name='amcl',
            output='screen',
            parameters=[nav2_yaml]
        ),
        
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[controller_yaml],
            remappings=[
                ('/cmd_vel', '/fastbot_1/cmd_vel'),
            ]),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[planner_yaml]),
            
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            parameters=[recovery_yaml],
            output='screen',
            remappings=[
                ('/cmd_vel', '/fastbot_1/cmd_vel'),
            ]),

        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[bt_navigator_yaml]),

        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_pathplanner',
            output='screen',
            parameters=[{'autostart': True},
                        {'node_names': ['map_server',
                                        'amcl',
                                        'planner_server',
                                        'controller_server',
                                        'behavior_server',
                                        'bt_navigator',
                                        'filter_mask_server',
                                        'costmap_filter_info_server']}]),
        
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_file],
            parameters=[{'use_sim_time': True}],
        ),
    ])
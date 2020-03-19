"""
The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
from games.arkanoid.communication import ( \
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop():
    """
    The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.
    ball_served = False

    # 2. Inform the game process that ml process is ready before start the loop.
    comm.ml_ready()

    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()

        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            ball_served = False

            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue

        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        if not ball_served:
            comm.send_instruction(scene_info.frame, PlatformAction.SERVE_TO_LEFT)
            ball_served = True
        else:
            ball_x=scene_info.ball[0]+2.5
            ball_y=scene_info.ball[1]
            platform_x=scene_info.platform[0]+20
            bias=ball_x-platform_x
            
            #ball speed 7  platform speed 5 (75,400)

            if(bias<0):
                bias*=-1

            should_plat=200-ball_x
            
            

        
            if(ball_y<300):
                if(should_plat>platform_x):
                    comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
                    if(ball_y<250&ball_y>200):
                        for x in range(0,2):
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                else:
                    comm.send_instruction(scene_info.frame,PlatformAction.MOVE_LEFT)
                    if(ball_y<250&ball_y>200):
                        for x in range(0,2):
                            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
            elif(ball_x>platform_x):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
            elif(ball_x<platform_x):
                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
            

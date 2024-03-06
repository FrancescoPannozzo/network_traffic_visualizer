""" Graphic visualizer
    use: 
    rendering 854x480 15FPS: manim -pql graphic_visualizer.py GraphicVisualizer/SwitchesInfo
    rendering 1280x720 60FPS: manim -pqm --fps 60 graphic_visualizer.py GraphicVisualizer/SwitchesInfo
    Faster rendering: manim -pql --disable_caching graphic_visualizer_test.py ClassName

"""

import logging
from manim import *
from utils import utils, graphic_visualizer_utils
from utils import CONSTANTS as CONST
from datetime import datetime, timedelta

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Adding one handler to manage the messages on a file
        logging.FileHandler('./log_files/graphic_visualizer_test_log.txt', mode='w'),
        # Adding one handler to see messages on console
        logging.StreamHandler()
    ]
)

class GraphicVisualizer(MovingCameraScene):
    """  Graph creator """

    def construct(self):
        start_test_time = datetime.now()
        # load network config
        network_data = utils.file_loader("./data/network")
        # load analyzed data file
        traffic_data = utils.file_loader("./data/analyzed_data_test")
        # load traffic colors
        traffic_perc_colors = utils.traffic_colors_gen()
      
        if network_data[CONST.NETWORK["SIM_PARAMS"]]["graphType"] == CONST.COMPLETE_GRAPH:
            logging.info("The graph type found is complete, rendering..")
            GraphicVisualizer.complete_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time)
        else:
            logging.info("The graph type found is mesh, rendering..")
            GraphicVisualizer.mesh_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time)
      
    def complete_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time):
        sim_params = traffic_data[CONST.ANALYZED_DATA["SIM_PARAMS"]]
       
        end_time = sim_params["simStartTime"] + timedelta(seconds=sim_params["simTime"])
        # show_delta is the time range we want to update the visualization
        show_delta = sim_params["updateDelta"]
        # time index to analyze
        time_walker = sim_params["simStartTime"] + timedelta(milliseconds=sim_params["averageDelta"])

        switches = []
        for s in network_data[CONST.NETWORK["SWITCHES"]]:
            switches.append(s["switchID"])

        logging.debug("switches: %s", switches)
        
        # extracting links data
        links = []
        for _, content in traffic_data[CONST.ANALYZED_DATA["TRAFFICS"]].items():
            links.append((content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B]))

        logging.debug("links: %s", links)

        font_size = 20
        if len(network_data[CONST.NETWORK["SWITCHES"]]) >= 100:
            font_size = 40

        phases = network_data[CONST.NETWORK["PHASES"]]
        phases_iterator = iter(phases.items())
        phase_time, phase = next(phases_iterator)
        logging.info("FIRST PHASE TIMESTAMP: %s", phase_time)
        # the sim time to visualize
        sim_time_txt = Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}", font="Courier New", font_size=font_size).set_color(YELLOW)
        phase_time_txt = Text(f"PHASE: {phase}", font="Courier New", font_size=font_size).set_color(YELLOW)
      
        #layout_scale = (len(switches))/3
        # graph creation
        grafo = Graph(switches, links, labels=True, layout="circular", layout_scale=2, vertex_config={"color":WHITE},
                      edge_config={"stroke_width": 10, "color":CONST.ZERO_TRAFFIC}
                      )
        
        self.play(Create(grafo))
        phase_time_txt.next_to(grafo, UP)
        sim_time_txt.next_to(phase_time_txt, UP)
        self.add(phase_time_txt)
        self.add(sim_time_txt)
        self.play(self.camera.auto_zoom([grafo, sim_time_txt, phase_time_txt], margin=1), run_time=0.5)
       
        # creating traffic animations
        traffic_count = 0
        while time_walker <= end_time:
            # temp LabeledDot structure
            animations = []
            # definig all the traffic color links at timeWalker time
            for _, content in traffic_data[CONST.ANALYZED_DATA["TRAFFICS"]].items():
                color_perc = int(content["traffic"][traffic_count])
                animations.append(grafo.edges[(content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B])].animate.set_color(traffic_perc_colors[color_perc]["hexValue"]))
            # playing animations
            if(time_walker == phase_time):
                self.play(*animations, Transform(sim_time_txt,
                                                Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                                font="Courier New",
                                                font_size=font_size).next_to(phase_time_txt, UP).set_color(YELLOW)),
                                        Transform(phase_time_txt,
                                                Text(f"PHASE: {phase}",
                                                font="Courier New",
                                                font_size=font_size).next_to(grafo, UP).set_color(YELLOW)),
                                    run_time=1
                                )
                try:
                    phase_time, phase = next(phases_iterator)
                except StopIteration:
                    logging.info("Phases ended")
            else:
                self.play(*animations, Transform(sim_time_txt,
                                                    Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                                        font="Courier New",
                                                        font_size=font_size).next_to(phase_time_txt, UP).set_color(YELLOW)),
                                                        run_time=1
                                            )
            
            traffic_count += 1
            # pushing forward sim time to check
            time_walker += timedelta(milliseconds=show_delta)
        self.wait(2)

        logging.info(graphic_visualizer_utils.get_test_duration(start_test_time))
    
    def mesh_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time):

        sim_params = traffic_data[CONST.ANALYZED_DATA["SIM_PARAMS"]]

        end_time = sim_params["simStartTime"] + timedelta(seconds=sim_params["simTime"])
        # show_delta is the time range we want to update the visualization
        show_delta = sim_params["updateDelta"]
        # time index to analyze
        time_walker = sim_params["simStartTime"] + timedelta(milliseconds=sim_params["averageDelta"])
       
        mesh = network_data[CONST.NETWORK["COORDINATES"]]["coordinates"]

        logging.debug("MESH: %s", mesh)
       
        # building mesh graph
        rows = len(mesh)
        cols = len(mesh[0])

        font_size = 20

        graph_mesh = {}
        # Nodes spacing
        spacing = 1
        if len(network_data[CONST.NETWORK["SWITCHES"]]) >= 100:
            spacing = 1.5
            font_size = 40


        phases = network_data[CONST.NETWORK["PHASES"]]
        phases_iterator = iter(phases.items())
        phase_time, phase = next(phases_iterator)
        logging.info("FIRST PHASE TIMESTAMP: %s", phase_time)
        # the sim time to visualize
        sim_time_txt = Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}", font="Courier New", font_size=font_size).set_color(YELLOW)
        phase_time_txt = Text(f"PHASE: {phase}", font="Courier New", font_size=font_size).set_color(YELLOW)
        
        # Creazione della griglia di nodi
        grid = VGroup()  # Gruppo per contenere tutti i nodi

        lines_grid = VGroup()
        mesh_grid = VGroup()

        for row in range(rows):
            for col in range(cols):
                opacity = 1
                # Switches with ID=0 are considered as empty spaces
                if str(mesh[row][col]) == "0":
                    opacity = 0
                dot = LabeledDot(str(mesh[row][col]), point=np.array([col * spacing, row * -spacing, 0]))
                dot.set_opacity(opacity)
                graph_mesh[mesh[row][col]] = dot
                #grid.add(dot)
                mesh_grid.add(dot)
        
        # extracting links data
        links = {}
        for _, content in traffic_data[CONST.ANALYZED_DATA["TRAFFICS"]].items():
            dot_a = graph_mesh[content["endpoints"][CONST.EP_A]]
            dot_b = graph_mesh[content["endpoints"][CONST.EP_B]]
            line = Line(dot_a.get_center(), dot_b.get_center(), color=CONST.ZERO_TRAFFIC, stroke_width=8)
            links[(content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B])] = line
            lines_grid.add(line)

        self.add(sim_time_txt)
        self.add(phase_time_txt)
        grid.add(lines_grid, mesh_grid)

        grid.move_to(ORIGIN)
        self.add(grid)
        phase_time_txt.next_to(grid, UP).set_color(YELLOW)
        sim_time_txt.next_to(phase_time_txt, UP).set_color(YELLOW)
        self.play(self.camera.auto_zoom([grid, sim_time_txt], margin=1), run_time=0.5)

        traffic_count = 0
        # creating traffic animations
        while time_walker <= end_time:
            # temp LabeledDot structure
            animations = []
            # definig all the traffic color links at timeWalker time
            for _, content in traffic_data[CONST.ANALYZED_DATA["TRAFFICS"]].items():
                color_perc = int(content["traffic"][traffic_count])
                animations.append(links[(content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B])].animate.set_color(traffic_perc_colors[color_perc]["hexValue"]))
            # playing animations

            traffic_count += 1
            if(time_walker == phase_time):
                self.play(*animations, Transform(sim_time_txt,
                                                Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                                font="Courier New",
                                                font_size=font_size).next_to(phase_time_txt, UP).set_color(YELLOW)),
                                        Transform(phase_time_txt,
                                                Text(f"PHASE: {phase}",
                                                font="Courier New",
                                                font_size=font_size).next_to(mesh_grid, UP).set_color(YELLOW)),
                                    run_time=1
                                )
                try:
                    phase_time, phase = next(phases_iterator)
                except StopIteration:
                    logging.info("Phases ended")
            else:
                self.play(*animations, Transform(sim_time_txt,
                                    Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                    font="Courier New",
                                    font_size=font_size).next_to(phase_time_txt, UP).set_color(YELLOW)),
                                    run_time=1
                                )
            # pushing forward sim time to check
            time_walker += timedelta(milliseconds=show_delta)
        

        self.wait(5)
        logging.info(graphic_visualizer_utils.get_test_duration(start_test_time))


class SwitchesInfo(MovingCameraScene):
    """  Graph creator """   

    def construct(self):
        # load network config
        network_data = utils.file_loader("./data/network")

        switches = network_data[CONST.NETWORK["SWITCHES"]]

        prev_dot = Text("SWITCHES:", font_size=17)
        for content in switches:
            if(content['switchID']) == "0":
                continue
            dot_text = Text(f"ID:{content['switchID']}", font="Courier New", font_size=15, color=BLACK)
            dot = LabeledDot(dot_text)
            text = Text(f"Name: {content['switchName']}\nIP: {content['address']}", font="Courier New", font_size=7)
            dot.next_to(prev_dot, RIGHT)
            text.next_to(dot, DOWN)
            self.add(dot, text)
            prev_dot = dot
            self.play(self.camera.auto_zoom([dot, text], margin=1), FadeIn(dot), FadeIn(text), run_time=2)

        self.wait()

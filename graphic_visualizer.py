""" Graphic visualizer
    use: 
    rendering 854x480 30FPS: manim -pql graphic_visualizer.py GraphicVisualizer/SwitchesInfo
    rendering 1280x720 60FPS: manim -pqm --fps 60 graphic_visualizer.py GraphicVisualizer/SwitchesInfo
    Faster rendering: manim -pql --disable_caching graphic_visualizer.py ClassName
    Reducing fps: manim -pql --fps 15 --disable_caching graphic_visualizer.py GraphicVisualizer

"""

import logging
from manim import *
from utils import utils, graphic_visualizer_utils
from utils import CONSTANTS as CONST
from datetime import datetime, timedelta
import math
import sys

# Logger config
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        # Adding one handler to manage the messages on a file
        logging.FileHandler('./log_files/graphic_visualizer_log.txt', mode='w'),
        # Adding one handler to see messages on console
        logging.StreamHandler()
    ]
)

class GraphicVisualizer(MovingCameraScene):
    """  Graph creator """

    def construct(self):
        # loadind date time for testing purpose
        start_test_time = datetime.now()
        # load network config
        network_data = utils.file_loader("./data/network")
        # load analyzed data file
        traffic_data = utils.file_loader("./data/analyzed_data")
        # load traffic colors
        traffic_perc_colors = None
        if network_data[CONST.NETWORK["SIM_PARAMS"]]["colorblind"] == "yes":
            # starting from color '##FFFFFF' low traffic, '##05FF00' mid traffic, '##FF05FF' full traffic
            traffic_perc_colors = graphic_visualizer_utils.traffic_colors_gen_colorblind()
        else:
            # starting from color '#05ff00' low traffic,'#fffa00' mid traffic, '#ff0500' full traffic
            r = 0
            g = 255
            b = 0
            traffic_perc_colors = graphic_visualizer_utils.traffic_colors_gen(r, g, b)
      
        if network_data[CONST.NETWORK["SIM_PARAMS"]]["graphType"] == CONST.COMPLETE_GRAPH:
            logging.info("The graph type found is complete, rendering..")
            GraphicVisualizer.complete_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time)
        else:
            logging.info("The graph type found is not complete, rendering..")
            GraphicVisualizer.mesh_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time)
      
    def complete_graph(self, network_data, traffic_data, traffic_perc_colors, start_test_time):
        sim_params = traffic_data[CONST.ANALYZED_DATA["SIM_PARAMS"]]
       
        end_time = sim_params["simStartTime"] + timedelta(seconds=sim_params["simTime"])
        # show_delta is the time range we want to update the visualization
        show_delta = sim_params["updateDelta"]
        # time index to analyze
        time_walker = sim_params["simStartTime"] + timedelta(milliseconds=sim_params["averageDelta"])
        # extracting switches
        switches = []
        for s in network_data[CONST.NETWORK["SWITCHES"]]:
            switches.append(s["switchID"])

        logging.debug("switches: %s", switches)
        
        # extracting links data
        links = []
        for content in traffic_data[CONST.ANALYZED_DATA["TRAFFICS"]]:
            links.append((content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B]))

        logging.debug("links: %s", links)

        # link-line stroke
        stroke_width = 4
        font_size = 20

        START_COLOR = traffic_perc_colors[0]['hexValue']
        if len(network_data[CONST.NETWORK["SWITCHES"]]) >= 100:
            font_size = 40
        if len(network_data[CONST.NETWORK["SWITCHES"]]) >= 20:
            stroke_width = 1


        phases = network_data[CONST.NETWORK["PHASES"]]
        phases_iterator = iter(phases.items())
        phase_time, phase = next(phases_iterator)
        logging.info("FIRST PHASE TIMESTAMP: %s", phase_time)
        # the sim time to visualize
        sim_time_txt = Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}", font="Courier New", font_size=font_size).set_color(WHITE)
        phase_time_txt = Text(f"PHASE: {phase}", font="Courier New", font_size=font_size).set_color(WHITE)
      
        # graph creation
        grafo = Graph(switches, links, labels=True, layout="circular", layout_scale=math.sqrt(len(switches)), vertex_config={"color":WHITE},
                      edge_config={"stroke_width": stroke_width, "color":START_COLOR}
                      )
        
        infos = GraphicVisualizer.show_info(self, sim_params, network_data, grafo, font_size)

        phase_time_txt.next_to(grafo, UP)
        sim_time_txt.next_to(phase_time_txt, UP/3)

        self.add(phase_time_txt)
        self.add(sim_time_txt)
        self.add(infos)
        self.play(Create(grafo))
        self.play(self.camera.auto_zoom([grafo, sim_time_txt, phase_time_txt, infos], margin=1), run_time=0.5)
       
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
                                                font_size=font_size).next_to(phase_time_txt, UP/3).set_color(WHITE)),
                                        Transform(phase_time_txt,
                                                Text(f"PHASE: {phase}",
                                                font="Courier New",
                                                font_size=font_size).next_to(grafo, UP).set_color(WHITE)),
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
                                                        font_size=font_size).next_to(phase_time_txt, UP/3).set_color(WHITE)),
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

        font_size = 10

        graph_mesh = {}
        # Nodes spacing
        spacing = 1.3

        # dynamic font-size scaling
        if cols > 4:
            font_size = font_size + 1.6 * (cols - 4)

        phases = network_data[CONST.NETWORK["PHASES"]]
        phases_iterator = iter(phases.items())
        phase_time, phase = next(phases_iterator)
        logging.info("FIRST PHASE TIMESTAMP: %s", phase_time)
        # the sim time to visualize
        sim_time_txt = Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}", font="Courier New", font_size=font_size).set_color(WHITE)
        phase_time_txt = Text(f"PHASE: {phase}", font="Courier New", font_size=font_size).set_color(WHITE)

        #infos = graphic_visualizer_utils.set_sim_infos(traffic_data[CONST.ANALYZED_DATA["SIM_PARAMS"]], font_size)

        # Creating the switches grid
        grid = VGroup() # Group to contain all the objects

        lines_grid = VGroup()
        mesh_grid = VGroup()
        EMPTY_SPACE = "0"

        for row in range(rows):
            for col in range(cols):
                opacity = 1
                # Switches with ID=0 are considered as empty spaces
                if str(mesh[row][col]) == EMPTY_SPACE:
                    opacity = 0
                # radius=0.45 o maggiore per opzione
                dot = LabeledDot(str(mesh[row][col]), point=np.array([col * spacing, row * -spacing, 0]))
                dot.set_opacity(opacity)
                graph_mesh[mesh[row][col]] = dot
                mesh_grid.add(dot)

        # extracting links
        data_links = {}
        for content in traffic_data[CONST.ANALYZED_DATA["TRAFFICS"]]:
            data_links[(content["endpoints"][CONST.EP_A], content["endpoints"][CONST.EP_B])] = content["traffic"]

        vertical_links = []
        horizontal_links = []
        if network_data[CONST.NETWORK["SIM_PARAMS"]]["graphType"] == CONST.TORUS_GRAPH:
            try:
                if rows > 2:
                    for i in range(cols):
                        if mesh[0][i] != 0 and mesh[rows-1][i] != 0:
                            if (mesh[0][i], mesh[rows-1][i]) not in data_links:
                                print("link contrario trovato?", (mesh[rows-1][i], mesh[0][i]) in data_links)
                                traffic =  data_links[(mesh[rows-1][i], mesh[0][i])]
                                data_links.pop((mesh[rows-1][i], mesh[0][i]))
                                data_links[(mesh[0][i], mesh[rows-1][i])] = traffic
                            vertical_links.append((mesh[0][i], mesh[rows-1][i]))
                if cols > 2:
                    for i in range(rows):
                        if mesh[i][0] != 0 and mesh[i][cols-1] != 0:
                            if (mesh[i][0], mesh[i][cols-1]) not in data_links:
                                print("link contrario trovato?", (mesh[i][cols-1], mesh[i][0]) in data_links)
                                traffic =  data_links[(mesh[i][cols-1], mesh[i][0])]
                                data_links.pop((mesh[i][cols-1], mesh[i][0]))
                                data_links[(mesh[i][0], mesh[i][cols-1])] = traffic
                            horizontal_links.append((mesh[i][0], mesh[i][cols-1]))
            except KeyError as e:
                logging.error("The arc %s is not present in the user data, please check your custom setting yaml file", e)
                logging.info("Exiting program now")
                sys.exit()

        START_COLOR = traffic_perc_colors[0]['hexValue']

        logging.debug("Printing data_links:")
        for l in data_links:
            logging.debug(l)
        
        # extracting links data
        links = {}
        for link, content in data_links.items():
            dot_a = graph_mesh[link[CONST.EP_A]]
            dot_b = graph_mesh[link[CONST.EP_B]]
            line = None
            if (link[CONST.EP_A], link[CONST.EP_B]) in vertical_links:
                dot_a_coord = dot_a.get_center()
                dot_a_coord[0] -= 0.5
                dot_a_coord[1] -= 0.5
                dot_b_coord = dot_b.get_center()
                dot_b_coord[0] -= 0.5
                dot_b_coord[1] += 0.5
                points = [dot_a.get_center(), dot_a_coord, dot_b_coord, dot_b.get_center()]
                line = VMobject(stroke_width=2).set_points_as_corners(points)
                line.set_color(START_COLOR)
            elif (link[CONST.EP_A], link[CONST.EP_B]) in horizontal_links:
                dot_a_coord = dot_a.get_center()
                dot_a_coord[0] += 0.6
                dot_a_coord[1] -= 0.6
                dot_b_coord = dot_b.get_center()
                dot_b_coord[0] -= 0.8
                dot_b_coord[1] -= 0.6
                points = [dot_a.get_center(), dot_a_coord, dot_b_coord, dot_b.get_center()]
                line = VMobject(stroke_width=2).set_points_as_corners(points)
                line.set_color(START_COLOR)
            else:
                line = Line(dot_a.get_center(), dot_b.get_center(), color=START_COLOR, stroke_width=8)
            links[(link[CONST.EP_A], link[CONST.EP_B])] = line
            lines_grid.add(line)

        #GraphicVisualizer.intro(self, sim_params, network_data)
        
        for link, content in data_links.items():
            print(link)
        
        grid.add(lines_grid, mesh_grid)

        grid.move_to(ORIGIN)
        sim_time_txt.move_to(ORIGIN)
        phase_time_txt.move_to(ORIGIN)
        phase_time_txt.next_to(grid, UP).set_color(WHITE)
        sim_time_txt.next_to(phase_time_txt, UP/3).set_color(WHITE)

        self.add(grid)
        self.add(phase_time_txt)
        self.add(sim_time_txt)

        infos = GraphicVisualizer.show_info(self, sim_params, network_data, grid, font_size)
        
        self.play(FadeIn(infos), FadeIn(grid), FadeIn(sim_time_txt), FadeIn(phase_time_txt), self.camera.auto_zoom([grid, sim_time_txt, phase_time_txt, infos], margin=1), run_time=0.5)

        traffic_count = 0
        # creating traffic animations
        while time_walker <= end_time:
            # temp LabeledDot structure
            animations = []
            # definig all the traffic color links at timeWalker time
            for link, content in data_links.items():
                color_perc = int(content[traffic_count])
                animations.append(links[(link[CONST.EP_A], link[CONST.EP_B])].animate.set_color(traffic_perc_colors[color_perc]["hexValue"]))
            # playing animations

            traffic_count += 1
            if(time_walker == phase_time):
                self.play(*animations, Transform(sim_time_txt,
                                                Text(f"SIM TIME: {time_walker.strftime('%H:%M:%S.%f')[:-3]}",
                                                font="Courier New",
                                                font_size=font_size).next_to(phase_time_txt, UP/3).set_color(WHITE)),
                                        Transform(phase_time_txt,
                                                Text(f"PHASE: {phase}",
                                                font="Courier New",
                                                font_size=font_size).next_to(grid, UP).set_color(WHITE)),
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
                                            font_size=font_size).next_to(phase_time_txt, UP/3).set_color(WHITE)),
                                        run_time=1
                                )
            # pushing forward sim time to check
            time_walker += timedelta(milliseconds=show_delta)

        self.wait(5)
        logging.info(graphic_visualizer_utils.get_test_duration(start_test_time))

    def show_info(self, sim_params, network_data, grid, font_size):
        net_sim_par = network_data[CONST.NETWORK["SIM_PARAMS"]]
        capacity = net_sim_par['linkCap']
        graph_type = net_sim_par['graphType']

        if net_sim_par['graphType'] == CONST.FREE_GRAPH:
            graph_type = "custom"

        tex = Text(f"{net_sim_par['simTime']} sec sim time, {net_sim_par['startSimTime']}",
                    font="Courier New",
                    font_size=font_size).scale(1)
        tex2 = Text(f"{len(network_data[CONST.NETWORK['SWITCHES']])} switches, {graph_type} graph, {capacity} Mbps",
                    font="Courier New",
                    font_size=font_size).scale(1)
        tex3 = Text(f"{sim_params['averageDelta']}ms average delta, {sim_params['updateDelta']}ms update delta",
                    font="Courier New",
                    font_size=font_size).scale(1)

        tex.next_to(grid, DOWN)
        tex2.next_to(tex, DOWN/4)
        tex3.next_to(tex2, DOWN/4)

        return Group.add(tex, tex2, tex3)

    def intro(self, sim_params, network_data):
        dot = Dot(UP * 2 + LEFT, fill_opacity=0)
        self.add(dot)
        net_sim_par = network_data[CONST.NETWORK["SIM_PARAMS"]]
        capacity = net_sim_par['linkCap']
        graph_type = net_sim_par['graphType']

        if net_sim_par['graphType'] == CONST.FREE_GRAPH:
            capacity = "mixed"
            graph_type = "custom"

        tex = Tex(f"{net_sim_par['simTime']} seconds simulation time, ", f"{net_sim_par['startSimTime']}").scale(1)
        tex2 = Tex(f"{len(network_data[CONST.NETWORK['SWITCHES']])} switches, ", f"{graph_type} graph, ", f"{capacity} Mbps").scale(1)
        tex3 = Tex(f"{sim_params['averageDelta']}ms average delta, ", f"{sim_params['updateDelta']}ms update delta").scale(1)
        tex2.next_to(tex, DOWN)
        tex3.next_to(tex2, DOWN)
        animations = [
            FadeIn(tex[0]),
            FadeIn(tex[1], shift=DOWN),
            FadeIn(tex2[0]),
            FadeIn(tex2[1], target_position=dot),
            FadeIn(tex2[2], shift=UP),
            FadeIn(tex3[0]),
            FadeIn(tex3[1], scale=1.5)
        ]
        
        self.play(AnimationGroup(*animations, lag_ratio=0.2))
        self.wait(3)
        animations = [
            FadeOut(tex[0]),
            FadeOut(tex[1], shift=DOWN),
            FadeOut(tex2[0]),
            FadeOut(tex2[1], target_position=dot),
            FadeOut(tex2[2], shift=UP),
            FadeOut(tex3[0]),
            FadeOut(tex3[1], scale=1.5)
        ]
        self.play(AnimationGroup(*animations, lag_ratio=0.2))


class SwitchesInfo(MovingCameraScene):

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


class NetworkData(MovingCameraScene):
    def construct(self):
        network_data = utils.file_loader("./data/network")
        switches = {}
        links = network_data[CONST.NETWORK["LINKS"]]

        for switch in network_data[CONST.NETWORK["SWITCHES"]]:
            switches[switch["switchID"]] = { "address": switch["address"], "switchName": switch["switchName"]}

        switch_to_show = []
        infos_to_show = []
        switch_show_count = 1
        switch_count = 1
        for switch_key, content in switches.items():
            dot = LabeledDot(str(switch_key))
            text = Text(f"Name: {content['switchName']}\nIP: {content['address']}", font="Courier New", font_size=20)
            switch_count += 1
            switch_to_show.append(dot)
            infos_to_show.append(text)
            if switch_show_count % 6 == 1:
                dot.to_edge(UP)
            else:
                dot.next_to(prev_text, DOWN)
            text.next_to(dot, DOWN)
            FadeIn(dot, text, shift=RIGHT)
            prev_text = text
            switch_show_count += 1
            self.play(FadeIn(dot, text, shift=LEFT), run_time=0.5)
            if switch_show_count == 6 or switch_count == len(switches)+1:
                switch_show_count = 1
                switch_animations = []
                text_animations = []
                for i in switch_to_show:
                    switch_animations.append(FadeOut(i, shift=LEFT))
                for i in infos_to_show:   
                    text_animations.append(FadeOut(i, shift=LEFT))
                self.wait(2)
                self.play(AnimationGroup(*switch_animations), AnimationGroup(*text_animations), run_time = 0.5)
                switch_to_show = []
                infos_to_show = []

        link_show_count = 1
        link_count = 1
        links_to_show = []
        y = 3.5
        for content in links:
            ep_a = LabeledDot(str(content["endpoints"][CONST.EP_A]))
            ep_b = LabeledDot(str(content["endpoints"][CONST.EP_B]))
            text = Text(f"{content['capacity']}", font="Courier New", font_size=20)
            link_count += 1
            if link_show_count % 9 == 1:
                ep_a.move_to([-3, y, 0])
                ep_b.move_to([3, y, 0])
            else:
                y -= 0.9
                ep_a.move_to([-3, y, 0])
                ep_b.move_to([3, y, 0])
            line = Line(ep_a, ep_b)
            text.next_to(line, DOWN)

            links_to_show.append(ep_a)
            links_to_show.append(ep_b)
            links_to_show.append(line)
            links_to_show.append(text)
            FadeIn(ep_a, ep_b, line, text, shift=RIGHT)
            link_show_count += 1
            self.play(FadeIn(ep_a, ep_b, line, text, shift=LEFT), run_time=0.5)
            if link_show_count == 9 or link_count == len(links)+1:
                link_show_count = 1
                links_animations = []
                for i in links_to_show:
                    links_animations.append(FadeOut(i, shift=LEFT))
                self.wait(2)
                self.play(AnimationGroup(*links_animations), run_time = 0.5)
                links_to_show = []
                y = 3.5

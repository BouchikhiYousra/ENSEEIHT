from manim import *
import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy import interpolate

import fourier
import debauchies_complexe as wvt
from utils import *



class Intro(Scene):

    def get_shape(self,tex):
        path = VMobject()
        shape = Tex(tex)
        for sp in shape.family_members_with_points():
            path.append_points(sp.get_points())
        return path

    def Segment(self, axes, previous_VGroup, rayon, CI, n, time):
        # Un segment est la liste [cercle, fleche, point] à un n donné
        centre = previous_VGroup[-1]
        
        circle = always_redraw(
        lambda : Circle(radius=rayon, color=BLUE, stroke_width=1).move_to(centre.get_center())
        )
        dot = always_redraw(
        lambda : Dot(color=RED, radius= DEFAULT_DOT_RADIUS/2).move_to(
            axes.c2p(
                axes.p2c(centre.get_center())[0] + rayon*np.cos(n*time.get_value() + CI),
                axes.p2c(centre.get_center())[1] + rayon*np.sin(n*time.get_value() + CI)
                )
            )
        )
        arrow = always_redraw(
            lambda : Arrow(
                circle.get_center(),
                dot.get_center(),
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.3
            )
        )
        
        previous_VGroup.add(circle, arrow, dot)

    def Segments(self, axes, cn, nb_segment, time):
        # Les segments forment un bras articulé consitué de nb_segment
        # et construit avec les cn les coefficients de Fourier
        segments = VGroup().add(axes)
        self.Segment(axes, segments, np.absolute(cn[0]), np.angle(cn[0]), 0, time)
        segments = segments[1:] # on enlève l'axe des segments
        for i in range(1,nb_segment+1):
            self.Segment(axes, segments, np.absolute(cn[i]), np.angle(cn[i]), (-1)**(i-1)*((i+1)//2), time)
        return segments

    def split_bras_articule(self, bras_articule):
        cercles = VGroup()
        fleches = VGroup()
        points = VGroup()
        for i in range(len(bras_articule)):
            if i%3==0:
                cercles.add(bras_articule[i])
            elif i%3==1:
                fleches.add(bras_articule[i])
            else:
                points.add(bras_articule[i])
        return cercles, fleches, points
    
    def afficher_chemin(self, pointeur):
        # Pour tracer le chemin du point sur le dernier segment
        path = VMobject(color=YELLOW, stroke_width=DEFAULT_STROKE_WIDTH/2)
        path.set_points_as_corners([pointeur.get_center(), pointeur.get_center()])
        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([pointeur.get_center()])
            path.become(previous_path)
        path.add_updater(update_path)
        self.add(path)
    
    def Motif(self, axes, previous_Vgroup, f_wvt, n, time):
        centre = previous_Vgroup[-1]
        chemin = f_wvt[n]
        taille = len(chemin)

        dot = always_redraw(
            lambda : Dot(color=RED, radius= DEFAULT_DOT_RADIUS/2).move_to(
                axes.c2p(
                    axes.p2c(centre.get_center())[0] + chemin[int(time.get_value()/5*taille)%taille].real,
                    axes.p2c(centre.get_center())[1] + chemin[int(time.get_value()/5*taille)%taille].imag
                )
            )
        )

        line_graph = axes.plot_line_graph(
            centre.get_center()[0] * np.ones(taille) + chemin.real,
            centre.get_center()[1] * np.ones(taille) + chemin.imag,
            line_color=WHITE,
            stroke_width = 2,
        )
        courbe = line_graph["line_graph"]
        vertex = line_graph["vertex_dots"]

        courbe.add_updater(lambda m : vertex[0].move_to(centre.get_center()))
        #line_graph.add_updater(lambda m : line_graph.move_to(centre.get_center()))

        arrow = always_redraw(
            lambda : Arrow(
                centre.get_center(),
                dot.get_center(),
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.3
            )
        )

        previous_Vgroup.add(courbe, arrow, dot)
        
    def Motifs(self, axes, f_wvt, time):
        motifs = VGroup().add(axes)
        self.Motif(axes, motifs, f_wvt, 0, time)
        motifs = motifs[1:]
        #nb_motifs = f_wvt.shape[0]
        nb_motifs = 2
        for n in range(1,nb_motifs):
            self.Motif(axes, motifs, f_wvt, n, time)
        return motifs

    def construct(self):

        time = ValueTracker(0)
        axes = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=8, y_length=6)
        
        # Fourier
        tex = "$\Sigma$"
        f_param_non_interpole = getTexComponents(tex)[0]
        #f_param_non_interpole = getDrawingComponents()[0]
        #f_param_non_interpole = getImageComponents("./chicken.jpg")[0]
        nb_point_param = 2**10
        f_param = interpolate.griddata(np.linspace(0,len(f_param_non_interpole),len(f_param_non_interpole)),f_param_non_interpole, np.linspace(0,len(f_param_non_interpole),nb_point_param), method='linear')
        
        
        
        coeffs_fourier = fourier.Cns(f_param, n_fourier_max=50, n_riemann=10_000)
        bras_articule = self.Segments(axes, coeffs_fourier, 50, time)
        path = self.afficher_chemin(bras_articule[-1])
        cercles, fleches, points = self.split_bras_articule(bras_articule)
        # Construction des animations manim
        self.play(Create(bras_articule))
        #self.add(path) est ajouté à la fonction afficher_chemin car si ajouté ici, ça donne un bug
        self.play(time.animate.set_value(10), rate_func=linear, run_time=10)
        self.wait(2)


"""
        # Debauchies complexe
        h = wvt.h_dbc()
        f_wvt = wvt.projection_complete(f_param, h, 5)
        f_wvt = f_wvt * 10**4
        nb, taille = f_wvt.shape
        aux = np.zeros(taille, dtype="complex")
        for i in range(nb):
            aux+= f_wvt[i]
        plt.scatter(aux.real, aux.imag)
        plt.show()

        points = VGroup()
        dot1 = Dot(ORIGIN, color=RED, radius= DEFAULT_DOT_RADIUS/2)
        points.add(dot1)
        fleches = VGroup()
        for i in range(2):
            points.add(always_redraw(lambda : Dot(color=RED, radius= DEFAULT_DOT_RADIUS/2).move_to(
                    axes.c2p(
                        axes.p2c(points[-1].get_center())[0] + f_wvt[i][int(time.get_value()/5*taille)%taille].real,
                        axes.p2c(points[-1].get_center())[1] + f_wvt[i][int(time.get_value()/5*taille)%taille].imag
                    )
                )
            ))
            #points.add(dot)

            arrow= always_redraw(lambda : Arrow(points[-2].get_center(), points[-1].get_center(), buff=0))
            fleches.add(arrow)

        self.add(points, fleches)
        self.afficher_chemin(points[-1])
        self.play(time.animate.set_value(8), rate_func=linear, run_time=10)
        self.wait(2)
"""
        


        

        
        
       
        

        



       
import numpy as np
import matplotlib.pyplot as plt
import cv2

class DrawingInterface:
    """ The Drawing Interface """
    def __init__(self, size = (780,780,3)):
        """Initiate the drawing interface.

        :param size: size of the drawing board, defaults to (780,780,3)
        :type size: tuple, optional
        """

        # Specify the callback function executed when we receive
        # mouse events/actions.
        cv2.namedWindow('Drawing Interface')
        cv2.setMouseCallback('Drawing Interface', self.draw)

        self.is_drawing = False      # true if mouse is pressed
        self.point = (None , None)   # last drawn point

        # Initialize the drawing board ::> black drawing board.
        self.drawing_board = np.zeros(size, np.uint8)
        
        # a single shape, temporary variable used to store a single shape
        # a shape starts when you click on the mouse and finishs when you
        # take your finger off.
        self.shape = []

        # store all shapes.
        self.shapes = []

        # lanch the drawing board
        self.launch(self.drawing_board)

        # Create and save the scatter plot of collected shapes
        # Purpose : Verify that the shapes we collected are correct
        ##########: and that they give the right image.
        self.output_image()


    # mouse callback function
    def draw(self, event, x, y, flags, param):
        """_summary_

        :param event: the mouse event.
        :type event: _type_
        :param x: first coordinate of the point
        :type x: float
        :param y: second coordinate of the point
        :type y: float
        :param flags: _description_
        :type flags: _type_
        :param param: _description_
        :type param: _type_
        """

        # When we click on the left button of the mouse.
        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_drawing = True
            self.point = x ,y
            self.shape.append(self.point)
            
        # When we move the mouse.
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_drawing == True:
                # if you are moving the mouse and at the same time clicking at the left
                # botton (is_drawing = True) then draw and save the shape.
                cv2.line(self.drawing_board, self.point, (x,y), color = (255,255,255), thickness = 3)
                self.point = x, y
                self.shape.append(self.point)

        # when we take our finger off the left button of the mouse.
        elif event == cv2.EVENT_LBUTTONUP:
            self.is_drawing = False
            cv2.line(self.drawing_board, self.point, (x,y), color=(255,255,255), thickness=3)

            # save the last point of the shape.
            self.point = x, y
            self.shape.append(self.point)

            # add the new shape to the list of shapes
            self.shapes.append(self.shape)

            # empty the list in order to create a new shape.
            self.shape = []

    # launch the drawing interface
    def launch(self, board):
        """Launch the drawing board, and draw with your mouse.

        :param board: Image (black image in this case) on top of which we will draw.
        :type board: numpy array.


        Note : to quit the interface click on : q
        """
        while(1):
            cv2.imshow('Drawing Interface', board)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def get_shapes(self,):
        """Get the shapes.

        :return: The list of shapes drawn.
        :rtype: List
        """
        return self.shapes

    def output_image(self,):
        """
        Plot the resulting points using a scatter plot in order
        to verify that we collected the right shapes.
        """
        x_values, y_values = [], []
        for shape in self.shapes:
            for pt in shape:
                x_values.append(pt[0])
                y_values.append(pt[1])
        plt.imshow(self.drawing_board)
        plt.scatter(x_values, y_values)
        plt.savefig('output.png')


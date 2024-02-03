from ezdxf.document import Drawing

from src.draw.base import BaseDxfBlock

class ShellBaseDxf:
    '''
    Базовый класс оболочки DXF, информацию с класса используют все виды оболочки (topside,leftside...)
    '''
    def __init__(self,shell_name):
        if isinstance(shell_name,str):
            self.shell_name = shell_name

class ShellSideDxf(BaseDxfBlock):

    def __init__(self,shell_block_name=None,status_painting_side=False,doc:Drawing=None):
        super().__init__(doc=doc)
        self.define_block_parametrs(block_name=shell_block_name)

        self.status_painting_side = painting_side #Если на стороне что-то рисуется, то нужно задать True

    def search_polyline(self):
        if self.status_painting_side == True:
            self.polyline = PolylineSurfaceOnSideDxf()
            self.polyline.set_main_coordinates(block=self.block)#задаются координаты Полилинии
            if '_' in self.block_name:
                self.polyline.side = self.block_name.split('_')[-1]#Имя стороны по последней части имени в блоке



class PolylineSurfaceOnSideDxf:

    def __init__(self):
        self._side = None
        self._x0 = None
        self._y0 = None
        self._x1 = None
        self._y1 = None

    @property
    def side(self):
        return self._side

    @side.setter
    def side(self,value):
        self._side = value

    def set_main_coordinates(self,block):
        '''
        Передача каждой координате данных
        :param surface_coordinates: {'xy0': [0.0, 8.0], 'xy1': [120.0, 71.8]}
        '''

        self.get_lwpolyline_coordinate(block=block)
        self.define_rectangle_size_for_inputs()
        if isinstance(self.surface_coordinates,dict):
            if self.surface_coordinates.__getitem__('xy0') and surface_coordinates.__getitem__('xy1'):
                self._x0 = self.surface_coordinates['xy0'][0]
                self._y0 = self.surface_coordinates['xy0'][1]
                self._x1 = self.surface_coordinates['xy1'][0]
                self._y1 = self.surface_coordinates['xy1'][1]


    def get_lwpolyline_coordinate(self,block):
        self.polyline_xy_coordinate_side = {'x': [], 'y': []}
        lwpolyline = block.query('LWPOLYLINE')[0]
        if lwpolyline is not None:
            lwpolyline.dxf.color = 255#чтобы все были белыми, если при добавлении в базу что-то случится
            for xy_coordinate in lwpolyline.get_points():
                self.polyline_xy_coordinate_side['x'].append(round(xy_coordinate[0], 1))
                self.polyline_xy_coordinate_side['y'].append(round(xy_coordinate[1], 1))
            self.polyline_xy_coordinate_side['x'] = tuple(sorted(set(self.polyline_xy_coordinate_side[side]['x'])))
            self.polyline_xy_coordinate_side['y'] = tuple(sorted(set(self.polyline_xy_coordinate_side[side]['y'])))
        else:
            raise BaseException('Нет полилинии в блоке')

    def define_rectangle_size_for_inputs(self):
        if hasattr(self,'polyline_xy_coordinate_side'):
            self.surface_coordinates = {}
            if len(self.polyline_xy_coordinate_side['y']) == 2:  # главное по высоте проверить
                return_dict['xy0'] = [self.polyline_xy_coordinate_side['x'][0], self.polyline_xy_coordinate_side['y'][0]]
                return_dict['xy1'] = [self.polyline_xy_coordinate_side['x'][1], self.polyline_xy_coordinate_side['y'][1]]
            else:
                return_dict['xy0'] = [self.polyline_xy_coordinate_side['x'][0], self.polyline_xy_coordinate_side['y'][-2]]
                return_dict['xy1'] = [self.polyline_xy_coordinate_side['x'][-1], self.polyline_xy_coordinate_side['y'][-1]]
        else:
            print('Непонятная ошибка draw.shell_side.dxf_shell.define_rectangle_size_for_inputs')

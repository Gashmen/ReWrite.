# from ezdxf.document import Drawing
import transliterate
from src.draw.base import DxfBase
# from src.draw.base import BaseDxfBlock

class ShellBaseDxf:
    '''
    Базовый класс оболочки DXF, информацию с класса используют все виды оболочки (topside,leftside...)
    shell_dict:
    {'Производитель': 'ВЗОР', 'Серия': 'ВП', 'Типоразмер': 161610, 'Взрывозащита': 'Exe', 'Материал': 'Пластик', 'Цвет(RAL)': 9005, 'Температура минимальная': -60, 'Температура максимальная': 130, 'IP': '66;67', 'Крепление': nan, '8': nan, '9': nan, '10': nan, 'Ширина': 160.0, 'Длина': 160.0, 'Глубина': 100.0, 'Масса': '0.73', 'Толщина стенки': '6', 'Зона Сверловки AB Ш': nan, 'Зона Сверловки БГ Ш': nan, 'Внутренние размеры AB': 120, 'Внутренние размеры БГ': 98, 'Межосевое расстояние для DIN': nan, 'Кол-во отверстий': nan, 'Расстояния болтов вдоль АВ': nan, 'Расстояния болтов вдоль БГ': nan, 'Количество болтов': nan, 'Внутренняя высота коробки': 75.0, 'Маркировка взрывозащиты': '1Ex e IIC;0Ex ia IIC;1Ex ib IIB;1Ex e[ia Ga] IIC;1Ex e mb IIC;1Ex e db IIC;1Ex e db mb IIC;1Ex e db [ia Ga] IIC;1Ex e db [ib] IIC;1Ex e mb ia IIC;1Ex e db mb ia IIC;--Ex tb IIIC;Ex ta IIIC;', 'Наличие': True}
    '''
    def __init__(self,shell_dict):
        if isinstance(shell_dict,dict):
            self.shell_dict = shell_dict

    def set_russian_name_shell(self):
        '''Получение русского имени оболочки'''
        if hasattr(self,'shell_dict'):
            self.shell_russian_name = self.shell_dict['Серия'] + '.' + str(self.shell_dict['Типоразмер'])
    def set_translit_name(self):
        '''Получение транслита имени'''
        if hasattr(self,'shell_russian_name'):
            self.shell_translit_name =  transliterate.translit(self.shell_russian_name, language_code='ru', reversed=True)

    def check_possible_to_draw(self,dxf_base:DxfBase):
        '''Проверка на наличие в базе dxf оболочки'''
        if isinstance(dxf_base,DxfBase):
            return dxf_base.check_shell(shell_translite_name=self.shell_translit_name)






# class ShellSideDxf(BaseDxfBlock):
#
#     def __init__(self,shell_block_name=None,status_painting_side=False,doc:Drawing=None):
#         super().__init__(doc=doc)
#         self.define_block_parametrs(block_name=shell_block_name)
#
#         self.status_painting_side = painting_side #Если на стороне что-то рисуется, то нужно задать True
#
#     def search_polyline(self):
#         if self.status_painting_side == True:
#             self.polyline = PolylineSurfaceOnSideDxf()
#             self.polyline.set_main_coordinates(block=self.block)#задаются координаты Полилинии
#             if '_' in self.block_name:
#                 self.polyline.side = self.block_name.split('_')[-1]#Имя стороны по последней части имени в блоке
#
#
#
# class PolylineSurfaceOnSideDxf:
#
#     def __init__(self):
#         self._side = None
#         self._x0 = None
#         self._y0 = None
#         self._x1 = None
#         self._y1 = None
#
#     @property
#     def side(self):
#         return self._side
#
#     @side.setter
#     def side(self,value):
#         self._side = value
#
#     def set_main_coordinates(self,block):
#         '''
#         Передача каждой координате данных
#         :param surface_coordinates: {'xy0': [0.0, 8.0], 'xy1': [120.0, 71.8]}
#         '''
#
#         self.get_lwpolyline_coordinate(block=block)
#         self.define_rectangle_size_for_inputs()
#         if isinstance(self.surface_coordinates,dict):
#             if self.surface_coordinates.__getitem__('xy0') and surface_coordinates.__getitem__('xy1'):
#                 self._x0 = self.surface_coordinates['xy0'][0]
#                 self._y0 = self.surface_coordinates['xy0'][1]
#                 self._x1 = self.surface_coordinates['xy1'][0]
#                 self._y1 = self.surface_coordinates['xy1'][1]
#
#
#     def get_lwpolyline_coordinate(self,block):
#         self.polyline_xy_coordinate_side = {'x': [], 'y': []}
#         lwpolyline = block.query('LWPOLYLINE')[0]
#         if lwpolyline is not None:
#             lwpolyline.dxf.color = 255#чтобы все были белыми, если при добавлении в базу что-то случится
#             for xy_coordinate in lwpolyline.get_points():
#                 self.polyline_xy_coordinate_side['x'].append(round(xy_coordinate[0], 1))
#                 self.polyline_xy_coordinate_side['y'].append(round(xy_coordinate[1], 1))
#             self.polyline_xy_coordinate_side['x'] = tuple(sorted(set(self.polyline_xy_coordinate_side[side]['x'])))
#             self.polyline_xy_coordinate_side['y'] = tuple(sorted(set(self.polyline_xy_coordinate_side[side]['y'])))
#         else:
#             raise BaseException('Нет полилинии в блоке')
#
#     def define_rectangle_size_for_inputs(self):
#         if hasattr(self,'polyline_xy_coordinate_side'):
#             self.surface_coordinates = {}
#             if len(self.polyline_xy_coordinate_side['y']) == 2:  # главное по высоте проверить
#                 return_dict['xy0'] = [self.polyline_xy_coordinate_side['x'][0], self.polyline_xy_coordinate_side['y'][0]]
#                 return_dict['xy1'] = [self.polyline_xy_coordinate_side['x'][1], self.polyline_xy_coordinate_side['y'][1]]
#             else:
#                 return_dict['xy0'] = [self.polyline_xy_coordinate_side['x'][0], self.polyline_xy_coordinate_side['y'][-2]]
#                 return_dict['xy1'] = [self.polyline_xy_coordinate_side['x'][-1], self.polyline_xy_coordinate_side['y'][-1]]
#         else:
#             print('Непонятная ошибка draw.shell_side.dxf_shell.define_rectangle_size_for_inputs')

if __name__ == '__main__':
    example_dict = {'Производитель': 'ВЗОР', 'Серия': 'ВП', 'Типоразмер': 161610, 'Взрывозащита': 'Exe', 'Материал': 'Пластик', 'Цвет(RAL)': 9005, 'Температура минимальная': -60, 'Температура максимальная': 130, 'IP': '66;67', 'Крепление': 'nan', '8': 'nan', '9': 'nan', '10': 'nan', 'Ширина': 160.0, 'Длина': 160.0, 'Глубина': 100.0, 'Масса': '0.73', 'Толщина стенки': '6', 'Зона Сверловки AB Ш': 'nan', 'Зона Сверловки БГ Ш': 'nan', 'Внутренние размеры AB': 120, 'Внутренние размеры БГ': 98, 'Межосевое расстояние для DIN': 'nan', 'Кол-во отверстий': 'nan', 'Расстояния болтов вдоль АВ': 'nan', 'Расстояния болтов вдоль БГ': 'nan', 'Количество болтов': 'nan', 'Внутренняя высота коробки': 75.0, 'Маркировка взрывозащиты': '1Ex e IIC;0Ex ia IIC;1Ex ib IIB;1Ex e[ia Ga] IIC;1Ex e mb IIC;1Ex e db IIC;1Ex e db mb IIC;1Ex e db [ia Ga] IIC;1Ex e db [ib] IIC;1Ex e mb ia IIC;1Ex e db mb ia IIC;--Ex tb IIIC;Ex ta IIIC;', 'Наличие': True}
    shell_base_dxf = ShellBaseDxf(example_dict)
    shell_base_dxf.set_russian_name_shell()
    shell_base_dxf.set_translit_name()
    print(shell_base_dxf.shell_translit_name)


from ezdxf.document import Drawing
import ezdxf
class DxfBase:

    def __init__(self,dxf_base_path):
        self.dxf_base_path = dxf_base_path

    def set_doc_dxf(self):
        if self.dxf_base_path != '':
            self.doc_base = ezdxf.readfile(self.dxf_base_path)

    def give_all_blocks(self):
        '''Получение словаря {имя блока:сам blocklayout}'''
        if hasattr(self,'doc_base'):
            self.doc_dict_blocks = {block.dxf.name:block for block in self.doc_base.blocks
                                                             if '*' not in block.dxf.name}

    def check_shell(self,shell_translite_name):
        '''Проверка возможности создания оболочки'''
        shell_block_names = ('topside','upside','downside',
                             'leftside','rightside','withoutcapside',
                             'cutside','installation_dimensions')

        possible_to_draw_shell = False
        if hasattr(self,'doc_dict_blocks'):
            for side_name in shell_block_names:
                block_name = shell_translite_name + '_' + side_name
                if block_name in self.doc_dict_blocks:
                    possible_to_draw_shell = True
                else:
                    possible_to_draw_shell = False
                    break
        return possible_to_draw_shell



dxf_base_path = 'D:\\Работа\\ReWrite\\information_for_testing\\DXF_BASE.dxf'
dxf_base = DxfBase(dxf_base_path=dxf_base_path)
dxf_base.set_doc_dxf()
dxf_base.give_all_blocks()

print(dxf_base.doc_dict_blocks)




class BaseDxfBlock:

    def __init__(self,doc:Drawing):

        self.block_name = None

        if isinstance(doc,Drawing):
            self.doc = doc

    def define_block_parametrs(self,block_name):
        self.set_block_dxf_name(block_name=block_name)
        if hasattr(self,'block_name'):
            self.get_block()
            self.define_extreme_lines()


    def set_block_dxf_name(self,block_name):
        if isinstance(block_name,str):
            self.block_name = block_name
        else:
            raise ValueError('BlockName задан не текстом в блоке BaseDxfBlock')

    def get_block(self):
        try:
            self.block = self.doc.blocks[self.block_name]
        except:
            raise BaseException(f'Нет данного блока в self.doc.blocks {self.doc}')

    def define_extreme_lines(self):
        '''Поиск координат крайних точек по линиям в блоке
        :block: Блок из doc.blocks
        :return:  {'x_max':max(x), 'y_max': max(y), 'x_min':min(x), 'y_min':min(y)}
        '''
        x = list()
        y = list()
        if hasattr(self,'block'):
            for line in self.block:
                if line.dxftype() == 'LINE':
                    x.append(line.dxf.start[0])
                    x.append(line.dxf.end[0])
                    y.append(line.dxf.start[1])
                    y.append(line.dxf.end[1])
            if x and y:  # если есть коробка
                self.extreme_lines =  {'x_max': max(x), 'y_max': max(y), 'x_min': min(x), 'y_min': min(y)}
        else:
            print('base.BaseDxfBlock.define_extreme_lines')











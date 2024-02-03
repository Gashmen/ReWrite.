from src.draw.base import BaseDxfBlock

class GlandDxf(BaseDxfBlock):

    def __init__(self,side_block, gland_name=None,status_painting_side=False,doc:Drawing=None):
        super().__init__(doc=doc)
        self.define_block_parametrs(block_name=shell_block_name)



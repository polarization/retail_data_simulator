from product.base_count import BaseCount


class Mini(BaseCount):

    def __init__(self, arena, position, in_district, in_possibility=0.95,
                 out_possibility=0.92):
        super(Mini, self).__init__(arena, position, in_district,
                                   in_possibility, out_possibility)
        self.product_name = 'Mini'

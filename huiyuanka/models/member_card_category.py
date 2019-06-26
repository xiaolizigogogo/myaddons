# -*- coding: utf-8 -*-

from odoo import models, fields, api


# 会员卡 实体
# 会员卡 类别 类别1 类别2 类别3 类别4 类别5
# 会员卡
class memberCardCategory(models.Model):
    _name = 'member.card.category'

    parent_id = fields.Many2one(comodel_name="member.card.category", string="memberCardCategory", required=False, index=True ,ondelete='cascade')

    name = fields.Char('Name', index=True, required=True, translate=True)

    code = fields.Char(string="Code", required=True)

    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)

    parent_path = fields.Char(index=True)

    child_id = fields.One2many('member.card.category', 'parent_id', 'Child Categories')

    member_card_count = fields.Integer(
        '# Products', compute='_compute_card_count',
        help="The number of memberCard under this category (Does not consider the children categories)")

    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    def _compute_product_count(self):
        read_group_res = self.env['member.card.template'].read_group([('categ_id', 'child_of', self.ids)], ['categ_id'], ['categ_id'])
        group_data = dict((data['categ_id'][0], data['categ_id_count']) for data in read_group_res)
        for categ in self:
            member_card_count = 0
            for sub_categ_id in categ.search([('id', 'child_of', categ.id)]).ids:
                member_card_count += group_data.get(sub_categ_id, 0)
            categ.product_count = member_card_count

# -*- coding: utf-8 -*-

from odoo import models, fields, api


# 会员卡 实体
# 会员卡 类别 类别1 类别2 类别3 类别4 类别5
# 会员卡
class memberCard(models.Model):
    _name = 'member.card'
    # 卡号
    card_num = new_field = fields.Text(string="card_num", required=False)
    # 等级
    template_id = fields.Many2one('member.card.template', 'id',required=False)
    # 余额
    rest_money = fields.Float(string="rest_money",  required=False)
    # 累计充值
    purchase_money = fields.Float(string="",  required=False)
    # 累计消费
    consumer_money = fields.Float(string="",  required=False)
    # 累计积分
    point = fields.Integer(string="",  required=False)
    # 所属客户
    partner_id = fields.Many2one('res.partner', 'id', required=False)
    #描述
    description = fields.Text()
    # 累计消费
    #
    @api.depends('value')
    def _value_pc(self):
        self.value2 = float(self.value) / 100

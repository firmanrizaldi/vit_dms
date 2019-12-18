# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
STATES =[('draft','Draft'),('progress','In Progress'),('done','Done')]

class muk_dms(models.Model):
	_name = 'muk_dms.file'
	_inherit = 'muk_dms.file'

	name = fields.Char(string="Version")
	tanggal = fields.Date(string="Tanggal Draft", default=lambda self: time.strftime("%Y-%m-%d"))
	status = fields.Selection(string="Status", selection=[
			('Draft', 'Draft'),
			('Open', 'Open'),
			('Done', 'Done')])
	state = fields.Selection(selection=STATES, string="State", required=False,
						readonly=True,
						compute="_get_state", help="")
	review_ids = fields.One2many('muk_dms.review','file_id', string='Review')
	reviewer_ids = fields.One2many('muk_dms.reviewer','file_id', string='Reviewer')
	info_ids = fields.One2many('muk_dms.info','file_id', string='Info')


	@api.depends('review_ids')
	def _get_state(self):
		"""
		jika belum ada review => state = draft
		jika sudah ada review => state = progress
		jika semua review done => state = done
		:return:
		"""
		for rec in self:
			if not rec.review_ids:
				final_state='draft'
			else:
				final_state = 'done'
				for review in rec.review_ids:
					if review.state != 'done':
						final_state = 'progress'

			rec.state = final_state

	@api.multi
	def action_draft(self):
		self.state = STATES[0][0]

	@api.multi
	def action_done(self):
		self.state = STATES[1][0]

class muk_dms_review(models.Model):
	_name = 'muk_dms.review'

	name = fields.Char(string="Bookmark",)
	tanggal_jam = fields.Datetime(string="Tanggal Jam", default=lambda self: time.strftime("%Y-%m-%d %H:%M:%S"))
	redaksi_asal = fields.Char(string="Redaksi Asal",)
	ulas = fields.Char(string="Ulasan",)
	file_id = fields.Many2one(comodel_name='muk_dms.file', string='File')
	user_id = fields.Many2one(comodel_name="res.users", string="Reviewer", required=False, default=lambda self: self.env.user.id)
	state = fields.Selection(string="State", selection=STATES, required=False, default=STATES[1][0])

class muk_dms_reviewer(models.Model):
	_name = 'muk_dms.reviewer'

	name = fields.Many2one(comodel_name="res.users", string="User", required=False, default=lambda self: self.env.user.id)
	file_id = fields.Many2one(comodel_name='muk_dms.file', string='File')
	state = fields.Char(string="State", compute="_get_state")

	@api.depends('file_id')
	def _get_state(self):
		"""
		state per masing-masing user reviewer

		jika belum melakukan review => state = draft
		jika sudah ada review => state = progress
		jika semua review done => state = done

		diambil dari muk_dms.file yang dilakukan oleh user_id

		:return:
		"""
		for rec in self:

			if not rec.file_id.review_ids:
				final_state = 'draft'
			else:
				final_state = 'done'
				for review in rec.file_id.review_ids:
					if review.state != 'done' and review.user_id == rec.name:
						final_state = 'progress'

			rec.state = final_state

class muk_dms_info(models.Model):
	_name = 'muk_dms.info'

	name = fields.Char(string="Nomor Naskah")
	tanggal_naskah = fields.Datetime(string="Tanggal Naskah", default=lambda self: time.strftime("%Y-%m-%d %H:%M:%S"))
	partner = fields.Many2one(comodel_name="res.partner", string="Partner")
	deskripsi = fields.Char(string="Deskripsi Naskah")
	file_id = fields.Many2one(comodel_name='muk_dms.file', string='File')
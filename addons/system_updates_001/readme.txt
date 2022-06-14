name: "System updates 001",
summary: Module update client.preassessment & pitch.polish.rating
description: This module will integrate additional method for reject business process within the submitted client.preassessment
the state field is also affected by this update together with the pitch.polish.rating.

important files within this module
==================================
/data/mail_templates.xml
/__manifest__.py
/__init__.py
/static/description/icon.png
/static/src/img/icon.png
/models/__init__.py
/models/pitch_polish_rating.py

This update must be applied with the change below:
on studio change the pitch.polish.rating.form from header to the following

<header>
     <button name="btn_refer" string="Refer" class="oe_highlight" type="object" attrs="{'invisible': [('state', '!=', 'new'),('state', '=', 'rejected')]}"/>
     <button name="btn_recommend" string="Recommend" class="oe_highlight" type="object" attrs="{'invisible': [('state', '!=', 'new'),('state', '=', 'rejected')]}"/>
     <button name="btn_reject" string="Reject" class="oe_highlight" type="object"  attrs="{'invisible': [('state', '=', 'rejected')]}"/>
     <field name="state" widget="statusbar" statusbar_visible="new,recommended"/>
</header>


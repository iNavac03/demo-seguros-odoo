Partner = env['res.partner']
tag = env['res.partner.category'].search([('name', '=', 'Asegurado')], limit=1)
template = env['mail.template'].search([('name', '=', 'Certificado emitido')], limit=1)

for rec in records:
    # 1) Crear o reutilizar al asegurado con los datos de importación
    if not rec.x_studio_partner_id and rec.x_studio_imp_nombre:
        curp = (rec.x_studio_imp_curp or '').strip().upper()
        partner = Partner
        if curp:
            partner = Partner.search([('x_studio_curp', '=', curp)], limit=1)

        vals = {'name': rec.x_studio_imp_nombre.strip()}
        if rec.x_studio_imp_rfc:
            vals['vat'] = rec.x_studio_imp_rfc.strip().upper()
        if curp:
            vals['x_studio_curp'] = curp
        if rec.x_studio_imp_fecha_nacimiento:
            vals['x_studio_fecha_nacimiento'] = rec.x_studio_imp_fecha_nacimiento
        if rec.x_studio_imp_telefono:
            vals['phone'] = rec.x_studio_imp_telefono
        if rec.x_studio_imp_correo:
            vals['email'] = rec.x_studio_imp_correo.strip()
        if rec.x_studio_imp_no_empleado:
            vals['x_studio_no_empleado'] = rec.x_studio_imp_no_empleado

        if partner:
            partner.write(vals)
        else:
            partner = Partner.create(vals)
        if tag:
            partner.write({'category_id': [(4, tag.id)]})
        rec.write({'x_studio_partner_id': partner.id})

    # 2) Generar el PDF si el certificado está Vigente
    if template and (rec.x_studio_estatus or '').lower() == 'vigente':
        rec.message_post_with_source(template, subtype_xmlid='mail.mt_note')
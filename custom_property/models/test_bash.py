def buscar_rango_not_self(self, days, property_id, tipo_tarifa):
    """
    Funcion para filtar la consulta dependiendo de los dias.
    Como resultado arroja como la respuesta de la consulta.
    """
    domain = [
        ('propiedad_id', '=', property_id),
        ('tipo_tarifa', '=', tipo_tarifa)
    ]
    
    if 1 <= days <= 7:
        domain.append(('tipo_renta', '=', 1))
    elif 8 <= days <= 30:
        domain.append(('tipo_renta', '=', 2))
    elif days > 30:
        domain.append(('tipo_renta', '=', 3))
    else:
        return False
    
    tarifa_dias = self.env['rental.rates'].search(domain)

    # If no rate is found for the given range, default to the daily rate
    if not tarifa_dias:
        daily_domain = domain[:-1]  # Remove the last added condition about the range
        daily_domain.append(('tipo_renta', '=', 1))
        tarifa_dias = self.env['rental.rates'].search(daily_domain)
    
    return tarifa_dias


def buscar_rango(self, days):
    """
    Funcion para filtar la consulta dependiendo de los dias.
    Como resultado arroja como la respuesta de la consulta.
    """
    domain = [
        ('propiedad_id', '=', self.property_id.id),
        ('tipo_tarifa', '=', self.tipo_tarifa)
    ]
    
    if 1 <= days <= 7:
        domain.append(('tipo_renta', '=', 1))
    elif 8 <= days <= 30:
        domain.append(('tipo_renta', '=', 2))
    elif days > 30:
        domain.append(('tipo_renta', '=', 3))
    else:
        return False
    
    tarifa_dias = self.env['rental.rates'].search(domain)

    # If no rate is found for the given range, default to the daily rate
    if not tarifa_dias:
        daily_domain = domain[:-1]  # Remove the last added condition about the range
        daily_domain.append(('tipo_renta', '=', 1))
        tarifa_dias = self.env['rental.rates'].search(daily_domain)
    
    return tarifa_dias

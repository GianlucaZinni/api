from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

# Define el formulario de registro utilizando WTForms
class RegistrationForm(FlaskForm):
    def validate_dni(form, field):
        dni = field.data.strip()
        if len(dni) < 7 or len(dni) > 8 or not dni.isdigit():
            raise validators.ValidationError("DNI argentino debe tener 7 u 8 dígitos numéricos.")

    dni = StringField("DNI", validators=[
        validators.InputRequired(message="El DNI es requerido"),  # DNI obligatorio
        validate_dni  # Llamada a la función de validación personalizada
    ])
    
    # Define una función de validación personalizada para el número de teléfono
    def validate_telefono(form, field):
        telefono = field.data.strip()
        if not telefono.startswith("+54 11 ") or not telefono[7:].isdigit() or len(telefono) != 15:
            raise validators.ValidationError("El número de teléfono debe estar en formato +54 11 XXXXXXXX")

    # Agrega el prefijo "+54 11 " al campo del número de teléfono y deshabilita la edición
    telefono = StringField("Telefono", default="+54 11 ", render_kw={"readonly": True}, validators=[validate_telefono])

    name = StringField("Nombre")
    surname = StringField("Apellido")
    submit = SubmitField("Registrar")
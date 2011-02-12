import settings
from flask import Flask

app = Flask('admin')
app.config.from_object(settings)

import models
import views


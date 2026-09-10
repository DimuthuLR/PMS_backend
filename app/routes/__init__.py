from .auth import auth_bp
from .plots import plots_bp
from .batches import batches_bp
from .care import care_bp
from .harvest import harvest_bp
from .financial import financial_bp
from .pest import pest_bp
from .tasks import tasks_bp
from .actuators import actuators_bp
from .tank import tank_bp
from .sensors import sensors_bp
from .weather import weather_bp
from .alerts import alerts_bp

# We'll import only the blueprints that exist so far.
# As we build more modules (care, harvest, financial, etc.),
# we'll add them here.

from .auth import auth_bp

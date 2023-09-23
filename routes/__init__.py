from flask import Flask

app = Flask(__name__)


#import routes.<<Filename>>
import routes.square
import routes.lazyDeveloper
import routes.greedyMonkey
import routes.digitalColony
import routes.railwayBuilder
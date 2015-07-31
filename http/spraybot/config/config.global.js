var config = module.exports = {};

// récupération des informations serveur
var os = require("os");
config.hostName = os.hostname();
config.hostType = os.type();
config.hostArch = os.arch();
config.hostVersion = os.release();

// nom de l'application
config.appName = "spraybot"
config.appTitle = "sprayBot"

// définition des chemins
config.rootDir = "/appli/http"

// récupération des informations du package.json
var pjson = require(config.rootDir + '/' + config.appName + '/package.json');
config.appVersion = pjson.version;

// http configuration
config.httpPort = 8080;

// configuration des pins du relay local
config.localRelay1 = 11;
config.localRelay2 = 12;

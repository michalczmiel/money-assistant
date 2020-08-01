provider "heroku" {
  version = "~>2.5"

  email   = var.email
  api_key = var.api_key
}

resource "random_password" "secret_key" {
  length = 16
}

resource "heroku_app" "app" {
  name   = var.app_name
  region = var.region

  config_vars = {
    DJANGO_SECRET_KEY = random_password.secret_key.result
    DJANGO_SETTINGS_MODULE = "money_assistant.settings.prod"
  }
}

resource "heroku_addon" "database" {
  app  = heroku_app.app.name
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_addon" "redis" {
  app  = heroku_app.app.name
  plan = "heroku-redis:hobby-dev"
}

resource "heroku_build" "build" {
  app = heroku_app.app.name
  buildpacks = ["https://github.com/heroku/heroku-buildpack-python"]

  source = {
    url = "https://github.com/michalczmiel/money-assistant/archive/${var.tag}.tar.gz"
  }

  depends_on = [heroku_addon.database, heroku_addon.redis]
}

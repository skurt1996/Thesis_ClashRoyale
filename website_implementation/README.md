Sensible data is redacted for privacy.
* Ruby version 3.2.2
* Custom installed gems: `devise 4.9`, `pagy 8.0`, `sassc-rails`
* run `bundle install` to install required gems in the Gemfile
* run `yarn install`
* edit `config/database.yml` to setup database credentials for MySQL
* run `rails db:migrate` to create and migrate database schema
* run `rails db:seed` to load the initial data into database
* if necessary adjust `.env` files and setup environment variables
* setup `RAILS_MASTER_KEY`
* precompile assets via `rails assets:precompile`
* start the server via `rails s`

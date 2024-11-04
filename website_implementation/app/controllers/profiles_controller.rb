class ProfilesController < ApplicationController
  before_action :authenticate_user!

  def show
    @user = current_user
    @pagy, @battles = pagy(@user.battles.distinct, items: 5)
  end
end
class BattlesController < ApplicationController
  before_action :authenticate_user!
  before_action :check_role

  def index
    @pagy, @battles = pagy(Battle.all, items: 5)
  end

  private

  def check_role
    unless current_user.role_id == 3 || current_user.role_id == 4
      redirect_to main_index_path, alert: 'You are not authorized to access this page.'
    end
  end

end

class MainController < ApplicationController

  def index
  end

  def privacy_policy
    render 'privacy-policy'
  end

  def terms_of_use
    render 'terms-of-use'
  end
end
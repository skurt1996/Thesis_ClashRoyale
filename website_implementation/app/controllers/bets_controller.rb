class BetsController < ApplicationController
  before_action :authenticate_user!

  def index
    # Find a random battle that the user has not bet on
    user_bets_battle_ids = current_user.bets.pluck(:battle_id)
    battles_without_user_bets = Battle.where.not(id: user_bets_battle_ids)
    @random_battle = battles_without_user_bets.order('RAND()').first
    # Klassenmethode von Battle machen!

    @bet = Bet.new
    @last_bet = current_user.bets.last
    @user = current_user

    # For our top list
    @top_users = User.all.sort_by(&:correct_bets_count).reverse.first(5)
  end

  def create
    @bet = Bet.new(bet_params)
    if @bet.save
      # Update attributes of the current_user
      current_user.increment!(:bets_count)
      update_correct_bets_count if bet_correct?(@bet)

      # Update instance variables for the frames
      @last_bet = @bet

      # Find a random battle that the user has not bet on
      user_bets_battle_ids = current_user.bets.pluck(:battle_id)
      battles_without_user_bets = Battle.where.not(id: user_bets_battle_ids)
      @random_battle = battles_without_user_bets.order('RAND()').first

      @user = current_user

      # For our top list
      @top_users = User.all.sort_by(&:correct_bets_count).reverse.first(5)

      respond_to(&:turbo_stream)
    else
      render :index
    end
  end

  private

  def bet_params
    params.require(:bet).permit(:bet, :battle_id).merge(user_id: current_user.id)
  end

  # Ins Modell
  def bet_correct?(bet)
    battle = bet.battle
    if bet.bet == 1
      battle.p1_crowns > battle.p2_crowns
    elsif bet.bet == 2
      battle.p2_crowns > battle.p1_crowns
    else
      false
    end
  end

  def update_correct_bets_count
    current_user.increment!(:correct_bets_count)
  end

end

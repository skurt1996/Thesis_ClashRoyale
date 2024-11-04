class AddBetCountsToUsers < ActiveRecord::Migration[7.1]
  def change
    add_column :users, :bets_count, :integer, default: 0
    add_column :users, :correct_bets_count, :integer, default: 0
  end
end

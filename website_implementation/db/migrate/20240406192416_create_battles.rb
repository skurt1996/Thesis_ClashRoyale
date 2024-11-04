class CreateBattles < ActiveRecord::Migration[7.1]
  def change
    create_table :battles do |t|
      t.datetime :battle_time
      t.string :game_mode
      t.string :p1_tag
      t.integer :p1_trophies
      t.integer :p1_best_trophies
      t.integer :p1_wins
      t.integer :p1_losses
      t.integer :p1_battle_count
      t.integer :p1_crowns
      t.float :p1_elixir_leaked
      t.json :p1_cards
      t.json :p1_support_cards
      t.string :p2_tag
      t.integer :p2_trophies
      t.integer :p2_best_trophies
      t.integer :p2_wins
      t.integer :p2_losses
      t.integer :p2_battle_count
      t.integer :p2_crowns
      t.float :p2_elixir_leaked
      t.json :p2_cards
      t.json :p2_support_cards

      t.timestamps
    end
  end
end

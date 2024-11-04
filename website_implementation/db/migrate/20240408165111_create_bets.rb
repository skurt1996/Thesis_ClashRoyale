class CreateBets < ActiveRecord::Migration[7.1]
  def change
    create_table :bets do |t|
      t.references :user, null: false, foreign_key: true
      t.references :battle, null: false, foreign_key: true
      t.integer :bet, limit: 1

      t.timestamps
    end
  end
end

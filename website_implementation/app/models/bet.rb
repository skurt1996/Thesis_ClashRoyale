class Bet < ApplicationRecord
  belongs_to :user
  belongs_to :battle

  validates :bet, inclusion: { in: [1, 2], message: "Bet must equal 1 or 2." }
end

class Battle < ApplicationRecord
  has_many :bets
  has_many :users, through: :bets
end
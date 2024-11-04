class User < ApplicationRecord
  belongs_to :role

  has_many :bets
  has_many :battles, through: :bets

  before_validation :set_default_role

  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable, :trackable and :omniauthable
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable

  validates :username, presence: true, uniqueness: true

  private
  def set_default_role
    self.role ||= Role.find_by_name('registered')
  end
end

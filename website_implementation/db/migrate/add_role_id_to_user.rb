# Deleted and recreated after some migrations problems
class AddRoleIdToUser < ActiveRecord::Migration[7.1]
  def change
    add_reference :users, :role, null: false, foreign_key: true
  end
end

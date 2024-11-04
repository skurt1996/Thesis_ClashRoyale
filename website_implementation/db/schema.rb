# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.1].define(version: 2024_04_08_195748) do
  create_table "battles", charset: "utf8mb4", collation: "utf8mb4_general_ci", force: :cascade do |t|
    t.datetime "battle_time"
    t.string "game_mode"
    t.string "p1_tag"
    t.integer "p1_trophies"
    t.integer "p1_best_trophies"
    t.integer "p1_wins"
    t.integer "p1_losses"
    t.integer "p1_battle_count"
    t.integer "p1_crowns"
    t.float "p1_elixir_leaked"
    t.text "p1_cards", size: :long, collation: "utf8mb4_bin"
    t.text "p1_support_cards", size: :long, collation: "utf8mb4_bin"
    t.string "p2_tag"
    t.integer "p2_trophies"
    t.integer "p2_best_trophies"
    t.integer "p2_wins"
    t.integer "p2_losses"
    t.integer "p2_battle_count"
    t.integer "p2_crowns"
    t.float "p2_elixir_leaked"
    t.text "p2_cards", size: :long, collation: "utf8mb4_bin"
    t.text "p2_support_cards", size: :long, collation: "utf8mb4_bin"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.check_constraint "json_valid(`p1_cards`)", name: "p1_cards"
    t.check_constraint "json_valid(`p1_support_cards`)", name: "p1_support_cards"
    t.check_constraint "json_valid(`p2_cards`)", name: "p2_cards"
    t.check_constraint "json_valid(`p2_support_cards`)", name: "p2_support_cards"
  end

  create_table "bets", charset: "utf8mb4", collation: "utf8mb4_general_ci", force: :cascade do |t|
    t.bigint "user_id", null: false
    t.bigint "battle_id", null: false
    t.integer "bet", limit: 1
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["battle_id"], name: "index_bets_on_battle_id"
    t.index ["user_id"], name: "index_bets_on_user_id"
  end

  create_table "roles", charset: "utf8mb4", collation: "utf8mb4_general_ci", force: :cascade do |t|
    t.string "name"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "users", charset: "utf8mb4", collation: "utf8mb4_general_ci", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "role_id", null: false
    t.string "username"
    t.integer "bets_count", default: 0
    t.integer "correct_bets_count", default: 0
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
    t.index ["role_id"], name: "index_users_on_role_id"
    t.index ["username"], name: "index_users_on_username", unique: true
  end

  add_foreign_key "bets", "battles"
  add_foreign_key "bets", "users"
end

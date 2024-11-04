module BattlesHelper
  def win_percentage(p1_wins, p1_losses)
    total_games = p1_wins + p1_losses
    return 0 if total_games.zero?

    percentage = (p1_wins.to_f / total_games) * 100
    number_with_precision(percentage, precision: 2)
  end

  # Eigene Bilder
  def cards(cards_json)
    cards = JSON.parse(cards_json)
    card_details = cards.map do |card|
      {
        name: card['name'],
        image_path: card['iconUrls']['medium']
      }
    end
  end
end
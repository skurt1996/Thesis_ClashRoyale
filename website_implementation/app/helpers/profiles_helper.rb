module ProfilesHelper
  def accuracy_rate(total_bets_count, correct_bets_count)
    return 0 if total_bets_count.zero?

    percentage = (correct_bets_count.to_f / total_bets_count) * 100
    number_with_precision(percentage, precision: 2)
  end
end
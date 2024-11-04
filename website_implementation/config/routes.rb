Rails.application.routes.draw do
  devise_for :users, controllers: {registrations: 'users/registrations'}

  root to: "main#index"
  get 'main/index'

  get 'profiles/show'
  get 'profile', to: 'profiles#show'

  get '/privacy-policy', to: 'main#privacy_policy'
  get '/terms-of-use', to: 'main#terms_of_use'

  resources :battles, only: [:index]

  resources :bets, only: %i[index create]
end

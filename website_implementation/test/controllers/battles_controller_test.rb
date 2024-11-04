require "test_helper"

class BattlesControllerTest < ActionDispatch::IntegrationTest
  test "should get index" do
    get battles_index_url
    assert_response :success
  end

  test "should get new" do
    get battles_new_url
    assert_response :success
  end

  test "should get create" do
    get battles_create_url
    assert_response :success
  end
end

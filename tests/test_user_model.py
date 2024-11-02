from view.add_user_view import AddUserView
from controller.add_user_controller import AddUserController
from view.delete_user_view import DeleteUserView
from controller.delete_user_controller import DeleteUserController
from view.edit_user_view import EditUserView
from controller.edit_user_controller import EditUserController
from view.user_list_view import UserListView
from controller.user_list_controller import UserListController
from view.print_list_view import PrintListView
from controller.print_list_controller import PrintListController

# Hàm kiểm tra sự kết nối giữa view và controller
def test_view_controller_interactions():
    # Tạo các instance của controller
    add_user_controller = AddUserController(None)
    delete_user_controller = DeleteUserController(None)
    edit_user_controller = EditUserController(None)
    user_list_controller = UserListController(None)
    print_list_controller = PrintListController(None)

    # Khởi tạo view với controller tương ứng
    add_user_view = AddUserView(None, add_user_controller)
    delete_user_view = DeleteUserView(None, delete_user_controller)
    edit_user_view = EditUserView(None, edit_user_controller)
    user_list_view = UserListView(None, user_list_controller)
    print_list_view = PrintListView(None, print_list_controller)

    # Kiểm tra xem view có chứa tham chiếu đến controller tương ứng hay không
    assert add_user_view.controller == add_user_controller, "AddUserView không được kết nối với AddUserController"
    assert delete_user_view.controller == delete_user_controller, "DeleteUserView không được kết nối với DeleteUserController"
    assert edit_user_view.controller == edit_user_controller, "EditUserView không được kết nối với EditUserController"
    assert user_list_view.controller == user_list_controller, "UserListView không được kết nối với UserListController"
    assert print_list_view.controller == print_list_controller, "PrintListView không được kết nối với PrintListController"

    print("Tất cả các view đều được kết nối với controller tương ứng.")

# Gọi hàm kiểm tra
test_view_controller_interactions()

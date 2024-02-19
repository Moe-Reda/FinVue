from .userRepository import UserRepository


class Login:
    userRepository = UserRepository()

    def login_user(self, username, password):
        try:
            data = self.userRepository.getUserData(username, password)
            if data is None:
                return {'message': 'User not found'}, 404
            elif password != data[3]:
                print(data[3], password)
                return {'message': 'Invalid login'}, 405
            return {'message': 'Login successful'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

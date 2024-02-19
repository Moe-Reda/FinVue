from .userRepository import UserRepository


class Register:
    userRepository = UserRepository()

    def register_user(self, email, username, password):
        try:
            self.userRepository.registerUser(email, username, password)
            return {'message': 'User registered successfully'}, 201
        except Exception as e:
            return {'error': str(e)}, 500

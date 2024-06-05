from database import session, UsersTable
from fast_api_app import Users
from sqlalchemy import select


class UsersRepository:
    @classmethod
    async def add_user(cls, user: Users):
        async with session() as new_session:
            user_dict = user.model_dump()
            user = Users(**user_dict)
            new_session.add(user)
            await new_session.flush()
            await new_session.commit()
            return user.id
        
    @classmethod
    async def select_user(cls):
        async with session() as new_session:
            query = select(UsersTable)
            result = await new_session.execute(query)
            users_models = result.scalars().all()
            return users_models
            
class RedisRepository:
    @classmethod
    async def add_email_verify_code(cls, email, code, redis):
        await redis.append(f'email_verify_{email}', code)
        await redis.close()

    @classmethod
    async def get_email_verify_code(cls, email, redis):
        code = await redis.get(f'email_verify_{email}')
        await redis.delete(f'email_verify_{email}')
        await redis.close()
        return code

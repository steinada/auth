async def add_email_verify_code(email, code, redis):
    await redis.append(f'email_verify_{email}', code)
    await redis.close()


async def get_email_verify_code(email, redis):
    code = await redis.get(f'email_verify_{email}')
    await redis.delete(f'email_verify_{email}')
    await redis.close()
    return code

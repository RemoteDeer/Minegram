async def create_table_users(db):
    sql = """
    CREATE TABLE IF NOT EXISTS users ( 
    user_id BIGINT PRIMARY KEY, 
    username TEXT, 
    role TEXT NOT NULL DEFAULT 'user' 
    );
    """
    try:
        await db.execute(sql)
        print("[DB] Table 'users' created or already exists")
    except Exception as e:
        print("[DB ERROR] Failed to create 'users':", e)

    await db.pool.execute(sql)

async def create_table_messages(db):
    sql = """
    CREATE TABLE IF NOT EXISTS messages ( 
    message_id BIGINT PRIMARY KEY, 
    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    text TEXT, user_id BIGINT NOT NULL, 
    
    CONSTRAINT fk_messages_user 
    FOREIGN KEY (user_id) 
    REFERENCES users (user_id) 
    ON DELETE CASCADE
    );
    """
    try:
        await db.execute(sql)
        print("[DB] Table 'messages' created or already exists")
    except Exception as e:
        print("[DB ERROR] Failed to create 'messages':", e)

    await db.pool.execute(sql)

async def create_table_requests(db):
    sql = """
    CREATE TABLE IF NOT EXISTS requests ( 
    request_id BIGINT PRIMARY KEY, 
    response_id BIGINT, 
    status TEXT NOT NULL, 
    user_id BIGINT NOT NULL, 

    CONSTRAINT fk_request_user 
    FOREIGN KEY (user_id) 
    REFERENCES users (user_id) 
    ON DELETE CASCADE, 
    
    CONSTRAINT fk_request_message 
    FOREIGN KEY (request_id) 
    REFERENCES messages (message_id) 
    ON DELETE CASCADE, 
    
    CONSTRAINT fk_response_message 
    FOREIGN KEY (response_id) 
    REFERENCES messages (message_id) 
    ON DELETE SET NULL
    );
    """

    try:
        await db.execute(sql)
        print("[DB] Table 'requests' created or already exists")
    except Exception as e:
        print("[DB ERROR] Failed to create 'requests':", e)

    await db.pool.execute(sql)

async def create_table_minecraft_worlds(db):
    sql = """
    CREATE TABLE IF NOT EXISTS minecraft_worlds ( 
    port INTEGER PRIMARY KEY, 
    name TEXT NOT NULL, password TEXT, 
    creator_id BIGINT, 

    CONSTRAINT fk_world_creator 
    FOREIGN KEY (creator_id) 
    REFERENCES users (user_id) 
    ON DELETE SET NULL
    );
    """

    try:
        await db.execute(sql)
        print("[DB] Table 'minecraft_worlds' created or already exists")
    except Exception as e:
        print("[DB ERROR] Failed to create 'minecraft_worlds':", e)

    await db.pool.execute(sql)

async def run(db):

    if not db.pool:
        raise ConnectionError("[DB ERROR] Database pool not initialized. Call db.connect() first!")

    await create_table_users(db)
    await create_table_messages(db)
    await create_table_requests(db)
    await create_table_minecraft_worlds(db)
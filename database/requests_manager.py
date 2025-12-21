from aiogram.utils.formatting import ExpandableBlockQuote

class RequestsManager:
    async def requests_add(self, user_id, text_req):
        sql = 'INSERT INTO requests (user_id, text_req) VALUES ($1, $2)'
        await self.execute(sql, user_id, text_req)
    
    async def requests_asnwer(self, request_id, status, text_req):
        sql = 'UPDATE requests SET status = $1, text_req = $2, answered_at = CURRENT_TIMESTAMP WHERE request_id = $3'
        return await self.execute(sql, status, text_req, request_id)
    

    async def get_total_requests(self, **kwargs):
        if kwargs:
            db_kwargs = {key: value for key, value, in kwargs.items() if key != 'username'}
            sql = "SELECT COUNT(*) FROM requests r"

            if 'username' in kwargs:
                sql += " JOIN users u ON r.user_id = u.user_id"
                db_kwargs['u.username'] = kwargs['username']

            sql += " WHERE "
            sql, parameters = self.format_args(sql, db_kwargs)
            return await self.fetchval(sql, *parameters)
        else:
            sql = "SELECT COUNT(*) FROM requests"
            return await self.fetchval(sql)

    async def get_paginated_requests(self, page = 1, per_page = 5, **kwargs):
        offset = per_page * (page - 1)

        total = await self.get_total_requests(**kwargs)
        total_pages = (total + per_page - 1) // per_page if total > 0 else 1

        sql = """
            SELECT 
                r.request_id,
                r.status,
                u.username,
                r.created_at,
                r.text_req,
                r.answered_at,
                r.text_ans
            FROM requests r 
            JOIN users u
                ON r.user_id = u.user_id
            """
        parameters = []

        if kwargs:
            db_kwargs = {key: value for key, value, in kwargs.items() if key != 'username'}
            sql += " WHERE "

            if 'username' in kwargs:
                db_kwargs['u.username'] = kwargs['username']
            
            sql, parameters = self.format_args(sql, db_kwargs)
            sql += f" ORDER BY r.created_at DESC LIMIT ${len(db_kwargs) + 1} OFFSET ${len(db_kwargs) + 2}"
            records = await self.fetch(sql, *parameters, per_page, offset)
        else:
            sql += " ORDER BY r.created_at DESC LIMIT $1 OFFSET $2"
            records = await self.fetch(sql, per_page, offset)
        
        return records, total_pages, total

    @staticmethod
    def truncate_text(text, max_len = 300):
        if not text:
            return ""
        if len(text) <= max_len:
            return text
        return text[:max_len-3] + '...'

    @staticmethod
    def format_status(status):
        status_map = {
            'open' : '🔓 OPEN',
            'processing': '⚙️ PROCESSING',
            'accepted' : '✅ COMPLETED',
            'rejected' : '🚫 REJECTED',
            'closed' : '🔒 CLOSED'
        }
        return status_map.get(status, '📝 UNKNOWN')

    @staticmethod
    def format_timestamp(timestamp):
        date_str = timestamp.strftime("%y-%m-%d")
        time_str = timestamp.strftime("%H:%M")

        return date_str, time_str

    async def format_page(self, page = 1, per_page = 5, **kwargs):
        records, total_pages, total = await self.get_paginated_requests(page=page, per_page=per_page, **kwargs)

        if not records:
            return None
        
        lines = [f"📄 Page {page} of {total_pages}\n"]

        active_filters = []
        if 'status' in kwargs:
            active_filters.append(f"Status: {kwargs['status']}")
        if 'user_id' in kwargs:
            active_filters.append(f"User ID: {kwargs['user_id']}")
        if 'username' in kwargs:
            active_filters.append(f"Username: {kwargs['username']}")

        if active_filters:
            lines.append(f"🔍 Filters: {', '.join(active_filters)}")
        
        lines.append("")

        for i, record in enumerate(records, start=per_page*(page-1) + 1):
            date_req, time_req = self.format_timestamp(record['created_at'])
            username = record['username']
            request_text = self.truncate_text(record['text_req'])
            status = self.format_status(record['status'])

            lines.append(
                f"#{i} 🆔 {record['request_id']} 👤 {username} {status} 🗓️ {date_req} ⏰ {time_req}"
                f"<blockquote expandable> {request_text} </blockquote>"
            )

            if record['text_ans'] and record['answered_at']:
                date_ans, time_ans = self.format_timestamp(record['answered_at'])
                response_text = self.truncate_text(record['text_ans'], max_len=20)
                lines.append(
                    f"<blockquote expandable> 🗓️ {date_ans} ⏰ {time_ans} \n {response_text} </blockquote>"
                )
            lines.append("")
            lines.append("")
        
        lines.append(f"📊 Total: {total} requests")

        return "\n".join(lines)
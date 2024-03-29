# !/usr/bin/env python
# -*- coding: utf-8 -*-

class InterfaceModel(object):
    @staticmethod
    def get_interface_list(cursor, condition, page=1, limit=10):
        """获取接口列表"""
        command = '''
        SELECT interface_id, interface_name, interface_desc, retry, is_deleted
        FROM tb_interface
        %s
        ORDER BY interface_id
        LIMIT :limit OFFSET :offset

        '''

        command = command % condition

        result = cursor.query(command, {
            'limit': limit,
            'offset': (page - 1) * limit
        })
        return result if result else []

    @staticmethod
    def get_interface_count(cursor, condition):
        """获取任务条数"""
        command = '''
        SELECT COUNT(*) AS count
        FROM tb_interface
        %s
        '''

        command = command % condition

        result = cursor.query_one(command)
        return result['count'] if result else 0

    @staticmethod
    def get_interface_detail(cursor, interface_id):
        """获取接口详情"""
        command = '''
        SELECT interface_id, interface_name, interface_desc, retry, is_deleted
        FROM tb_interface
        WHERE interface_id = :interface_id
        '''
        result = cursor.query_one(command, {
            'interface_id': interface_id
        })
        return result if result else {}

    @staticmethod
    def get_interface_graph(cursor, interface_id):
        """获取接口任务依赖"""
        command = '''
        SELECT a.interface_id, a.job_id, a.job_name,
        c.interface_id AS prep_interface_id, c.job_id AS prep_id, c.job_name AS prep_name
        FROM tb_jobs AS a
        LEFT JOIN tb_job_prep AS b ON a.job_id = b.job_id AND b.is_deleted = 0
        LEFT JOIN tb_jobs AS c ON b.prep_id = c.job_id
        WHERE a.interface_id = :interface_id AND a.is_deleted = 0
        '''

        result = cursor.query(command, {
            'interface_id': interface_id
        })

        # command = '''
        # SELECT b.InterfaceID AS interface_id, a.ScheduleID AS job_id, b.ScheduleComment AS job_name,
        # c.InterfaceID AS prep_interface_id, a.PreScheduleID AS prep_id, c.ScheduleComment AS prep_name
        # FROM etl.tconf_precondition AS a
        # LEFT JOIN etl.tconf_schedule AS b ON a.ScheduleID = b.ScheduleID
        # LEFT JOIN etl.tconf_schedule AS c ON a.PreScheduleID = c.ScheduleID
        # '''
        #
        # result = cursor.query(command)
        return result if result else []

    @staticmethod
    def update_interface_detail(cursor, interface_id, interface_name, interface_desc, retry, user_id, is_deleted):
        """修改接口详情"""
        command = '''
        UPDATE tb_interface
        SET interface_name = :interface_name, interface_desc = :interface_desc, retry = :retry,
        is_deleted = :is_deleted, updater_id = :user_id, update_time = UNIX_TIMESTAMP()
        WHERE interface_id = :interface_id
        '''
        result = cursor.update(command, {
            'interface_id': interface_id,
            'interface_name': interface_name,
            'interface_desc': interface_desc,
            'retry': retry,
            'is_deleted': is_deleted,
            'user_id': user_id
        })
        return result

    @staticmethod
    def add_interface(cursor, interface_name, interface_desc, retry, user_id):
        """新增接口"""
        command = '''
        INSERT INTO tb_interface(interface_name, interface_desc,
        insert_time, update_time, retry, creator_id, updater_id)
        VALUES(:interface_name, :interface_desc, UNIX_TIMESTAMP(),
        UNIX_TIMESTAMP(), :retry, :user_id, :user_id)
        '''

        result = cursor.insert(command, {
            'interface_name': interface_name,
            'interface_desc': interface_desc,
            'retry': retry,
            'user_id': user_id
        })
        return result

    @staticmethod
    def get_job_prep_by_interface(cursor, interface_id):
        """查询接口下任务被依赖"""
        command = '''
        SELECT a.job_id, b.job_id AS out_id
        FROM tb_jobs AS a
        LEFT JOIN tb_job_prep AS b ON a.job_id = b.prep_id AND b.is_deleted = 0
        WHERE a.interface_id = :interface_id AND a.is_deleted = 0
        '''

        result = cursor.query(command, {
            'interface_id': interface_id
        })
        return result if result else []

    @staticmethod
    def delete_interface(cursor, interface_id, user_id):
        """删除接口"""
        command = '''
        UPDATE tb_interface
        SET is_deleted = 1, updater_id = :user_id, update_time = UNIX_TIMESTAMP()
        WHERE interface_id = :interface_id
        '''

        result = cursor.delete(command, {
            'interface_id': interface_id,
            'user_id': user_id
        })
        return result

    @staticmethod
    def get_interface_id_list(cursor):
        """获取接口id列表"""
        command = '''
        SELECT interface_id, interface_name
        FROM tb_interface
        WHERE is_deleted = 0
        '''

        result = cursor.query(command)
        return result if result else []

    @staticmethod
    def get_schedule_detail(cursor, interface_id):
        """获取接口是否被调度"""
        command = '''
        SELECT dispatch_id, interface_id, dispatch_name, dispatch_desc,
        `minute`, `hour`, `day`, `month`, `week`, `status`
        FROM tb_dispatch
        WHERE interface_id = :interface_id AND `status` != 0
        '''
        result = cursor.query_one(command, {
            'interface_id': interface_id
        })
        return result if result else {}
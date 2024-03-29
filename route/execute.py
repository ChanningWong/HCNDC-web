# !/usr/bin/env python
# -*- coding: utf-8 -*-

from configs import app
from flask import render_template, session, redirect


@app.route('/execute/list/')
def ExecuteList():
    """执行列表"""
    if session.get('login'):
        return render_template('execute/execute_list.html')
    return redirect('/login/')


@app.route('/execute/detail/<int:id>/')
def ExecuteDetail(id):
    """执行详情"""
    if session.get('login'):
        return render_template('execute/execute_detail.html', exec_id=id)
    return redirect('login')


@app.route('/execute/log/<int:exec_id>/<int:job_id>/')
def ExecuteDetailLog(exec_id, job_id):
    """执行日志"""
    if session.get('login'):
        return render_template('execute/execute_log.html', exec_id=exec_id, job_id=job_id)
    return redirect('login')

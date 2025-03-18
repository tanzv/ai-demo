import React, { useState } from 'react';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { LoginFormPage, ProFormText } from '@ant-design/pro-components';
import { message, Spin } from 'antd';
import { useNavigate } from 'react-router-dom';
import authService from '../../services/auth';
import logo from '../../assets/logo.svg';
import './style.css';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (values: { username: string; password: string }) => {
    try {
      setLoading(true);
      const response = await authService.login(values);
      if (response.access_token) {
        message.success('登录成功！');
        navigate('/dashboard');
      }
    } catch (error: any) {
      message.error(error.response?.data?.error || '登录失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <Spin spinning={loading}>
          <LoginFormPage
            logo={logo}
            title="AI Demo"
            subTitle="基于 React 和 Ant Design 的 AI 演示系统"
            onFinish={async (values) => {
              await handleSubmit(values as { username: string; password: string });
            }}
            containerStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)',
              borderRadius: '12px',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
            }}
          >
            <ProFormText
              name="username"
              fieldProps={{
                size: 'large',
                prefix: <UserOutlined className="prefixIcon" />,
                placeholder: '请输入用户名',
              }}
              rules={[
                {
                  required: true,
                  message: '请输入用户名!',
                },
                {
                  min: 3,
                  message: '用户名至少3个字符!',
                },
              ]}
            />
            <ProFormText.Password
              name="password"
              fieldProps={{
                size: 'large',
                prefix: <LockOutlined className="prefixIcon" />,
                placeholder: '请输入密码',
              }}
              rules={[
                {
                  required: true,
                  message: '请输入密码！',
                },
                {
                  min: 6,
                  message: '密码至少6个字符!',
                },
              ]}
            />
          </LoginFormPage>
        </Spin>
      </div>
    </div>
  );
};

export default LoginPage; 
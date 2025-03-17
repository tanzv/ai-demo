import React from 'react';
import { PageContainer } from '@ant-design/pro-components';
import { Card, Row, Col, Statistic } from 'antd';
import { UserOutlined, RobotOutlined, ApiOutlined } from '@ant-design/icons';

const DashboardPage: React.FC = () => {
  return (
    <PageContainer>
      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <Statistic
              title="用户总数"
              value={1128}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="AI 模型数"
              value={3}
              prefix={<RobotOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="API 调用次数"
              value={11280}
              prefix={<ApiOutlined />}
            />
          </Card>
        </Col>
      </Row>
    </PageContainer>
  );
};

export default DashboardPage; 
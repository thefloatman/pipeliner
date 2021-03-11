#!/bin/sh

mongo localhost:27017/${MONGO_DB_NAME} <<-EOF
    rs.initiate({
        _id: "rs0",
        members: [ { _id: 0, host: getHostName() + ":27017" } ]
    });
EOF
echo "Initiated replica set"

sleep 5

mongo localhost:27017/${MONGO_ADMIN}  <<-EOF
    db.createUser({ 
        user: "${MONGO_ADMIN}", 
        pwd: "${MONGO_ADMIN}", 
        roles: [ { role: "userAdminAnyDatabase", db: "${MONGO_ADMIN}" } ] 
    });
    db.grantRolesToUser("${MONGO_ADMIN}", ["clusterManager"]);
EOF

mongo -u ${MONGO_ADMIN} -p ${MONGO_ADMIN} localhost:27017/${MONGO_ADMIN} <<-EOF
    db.runCommand({
        createRole: "listDatabases",
        privileges: [
            { resource: { cluster : true }, actions: ["listDatabases"]}
        ],
        roles: []
    });
    db.createUser({
        user: "${MONGO_DB_NAME}",
        pwd: "${MONGO_DB_NAME}",
        roles: [
            { role: "readWrite", db: "${MONGO_DB_NAME}" },
            { role: "readWrite", db: "test_${MONGO_DB_NAME}" },
            { role: "read", db: "local" },
            { role: "listDatabases", db: "${MONGO_ADMIN}" },
            { role: "read", db: "config" },
            { role: "read", db: "${MONGO_ADMIN}" }
        ]
    });
EOF
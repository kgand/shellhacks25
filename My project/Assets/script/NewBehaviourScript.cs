// using UnityEngine;

// public class PlayerController : MonoBehaviour
// {
//     private CharacterController controller;
//     private Vector3 playerVelocity;
//     private bool groundedPlayer;
//     [SerializeField] private float playerSpeed = 2.0f;
//     [SerializeField] private float jumpHeight = 1.0f;
//     [SerializeField] private float gravityValue = -9.81f;

//     private void Start()
//     {
//         controller = gameObject.GetComponent<CharacterController>();
//     }

//     void Update()
//     {
//         groundedPlayer = controller.isGrounded;
//         if (groundedPlayer && playerVelocity.y < 0)
//         {
//             playerVelocity.y = 0f;
//         }

//         // 获取键盘输入
//         float moveX = Input.GetAxis("Horizontal"); // A, D, 左箭头, 右箭头
//         float moveZ = Input.GetAxis("Vertical");   // W, S, 上箭头, 下箭头

//         Vector3 move = transform.right * moveX + transform.forward * moveZ;
//         controller.Move(move * playerSpeed * Time.deltaTime);

//         // 处理跳跃
//         if (Input.GetButtonDown("Jump") && groundedPlayer)
//         {
//             playerVelocity.y += Mathf.Sqrt(jumpHeight * -3.0f * gravityValue);
//         }

//         // 应用重力
//         playerVelocity.y += gravityValue * Time.deltaTime;
//         controller.Move(playerVelocity * Time.deltaTime);
//     }
// }